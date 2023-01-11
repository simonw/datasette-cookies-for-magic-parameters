from datasette import hookimpl
from datasette.utils import derive_named_parameters
import json

JS = """
function enhanceMagicParameterForm() {
    let params = PARAMS;
    let form = document.querySelector('form.sql');
    let paramsWithValues = document.cookie.split(';').filter(cookie => {
        return cookie.split('=')[1].replace(/"/g, '').trim()
    }).map(cookie => cookie.split('=')[0].trim());
    // Remove anything we added last time
    form.querySelectorAll('.magic-params').forEach(el => el.remove());
    params.forEach((name) => {
        let p = document.createElement('p');
        p.classList.add('magic-params');
        p.innerHTML = `<label style="width: unset; min-width: 15%" for="param-${name}">${name}</label> `;
        if (paramsWithValues.includes(name)) {
            // It has a value - provide a button to unset it
            p.innerHTML += `
              <span style="border: 1px solid #ccc; background-color: #eaeaea; border-radius: 3px; padding: 9px 16px 9px 4px; display: inline-block; font-size: 1em; font-family: Helvetica, sans-serif;">
              ****************</span> `;
            let button = document.createElement('button');
            button.setAttribute('type', 'button');
            button.innerText = 'Unset this value';
            button.dataset.name = name;
            p.appendChild(button);
            button.addEventListener('click', (event) => {
                event.preventDefault();
                // Read the name
                let name = event.target.dataset.name;
                // Remove the cookie
                document.cookie = name + '=; Path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                // Redraw the form
                enhanceMagicParameterForm();
            });
        } else {
            let inputs = `<input type="text" name="${name}" id="param-${name}">`;
            p.innerHTML += inputs;
        }
        form.appendChild(p);
    });
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        // Set cookies for each of PARAMS
        let formData = new FormData(event.target);
        // Set a cookie for each of the parameters
        formData.forEach((value, name) => {
            if (params.includes(name)) {
                document.cookie = name + '="' + value + '"; Path=/; SameSite=Lax';
                // Remove it from the form so it is not submitted to the server
                let input = form.querySelector(`input[name='${name}']`);
                input.setAttribute('disabled', 'on');
            }
        });
        event.target.submit();
    });
}
enhanceMagicParameterForm();
"""


@hookimpl
def extra_body_script(template, database, request, datasette):
    async def inner():
        if template != "query.html":
            return ""
        table = request.url_vars.get("table")
        if not table:
            return ""
        # Get the SQL for this query
        canned_query = await datasette.get_canned_query(database, table, request.actor)
        if not canned_query:
            return ""
        sql = canned_query["sql"]
        db = datasette.get_database(database)
        params = await derive_named_parameters(db, sql)
        cookie_params = [
            p[len("_cookie_") :] for p in params if p.startswith("_cookie_")
        ]
        if not cookie_params:
            return ""
        return JS.replace("PARAMS", json.dumps(list(set(cookie_params))))

    return inner


async def set_message():
    from datasette import Response

    response = Response.redirect("/-/asgi-scope")
    response.set_cookie("name_with_spaces", "name with spaces")
    return response


@hookimpl
def register_routes():
    return [
        ("/-/set-message", set_message),
    ]
