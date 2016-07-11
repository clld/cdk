<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "unitvalues" %>

<%def name="sidebar()">
    <div class="well">
        <h4>Language</h4>
        <p>
            ${ctx.language}
        </p>
        % if ctx.variants:
            <h4>Variants</h4>
            <dl>
                % for lang, vars in ctx.variants:
                    <dt>${lang}</dt>
                    <dd>
                        <ul>
                            % for var in vars:
                                <li>${h.link(request, var)}</li>
                            % endfor
                        </ul>
                    </dd>
                % endfor
            </dl>
        % endif
    </div>
</%def>

<h2>${'Variant' if ctx.variant else 'Headword'} ${u.form(ctx.name)} <sup>${ctx.disambiguation}</sup></h2>

<p>
    <i>${ctx.pos}</i>, <i>${ctx.aspect or ctx.plural}</i>
</p>
<ol>
    % for counterpart in ctx.unitvalues:
    <li>
        <strong>${counterpart.unitparameter.name} / ${counterpart.unitparameter.russian}</strong>
        <dl>
% for loc, examples in u.examples_by_location(counterpart):
    <dt>${loc or 'other'}</dt>
    <dd>
        <ul>
        % for ex in examples:
            <li>
                <i>${ex.name}</i><br/>
                ${ex.description}
                % if ex.language.name != 'Ket':
                (${ex.language})
                % endif
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
    </li>
    % endfor
</ol>
