<dl>
% for loc, examples in u.examples_by_location(ctx):
    <dt>${loc or 'other'}</dt>
    <dd>
        <ul>
        % for ex in examples:
            <li>
                <i>${ex.name}</i><br/>
                ${ex.description}
                % if ex.references:
                    <br/>
                    (${h.link(request, ex.references[0].source)}: ${ex.references[0].description})
                % endif
            </li>
        % endfor
        </ul>
    </dd>
% endfor
</dl>