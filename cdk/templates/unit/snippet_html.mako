<dl>
% for loc, examples in ctx.grouped_examples():
    <dt>${loc or 'other'}</dt>
    <dd>
        <ul>
        % for ex in examples:
            <li>
                <i>${ex.name}</i><br/>
                ${ex.description}
            </li>
        % endfor
        </ul>
    </dd>
% endfor
</dl>