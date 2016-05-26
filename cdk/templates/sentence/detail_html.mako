<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sentences" %>

<%def name="sidebar()">
    <div class="well">
        <dl>
            <dt>Variety:</dt>
            <dd>${h.link(request, ctx.language)}</dd>
            % if any(ex.location for ex in ctx.examples):
                <dt>Recorded in:</dt>
                <dd>
                    <ul class="unstyled">
                        % for loc in set(ex.location for ex in ctx.examples if ex.location):
                            <li>${loc}</li>
                        % endfor:
                    </ul>
                </dd>
            % endif
            % if ctx.references:
                <dt>Source:</dt>
                <dd>
                    <ul class="unstyled">
                        % for ref in ctx.references:
                        <li>${h.link(request, ref.source)}: ${ref.description}</li>
                        % endfor
                    </ul>
                </dd>
            % endif
        </dl>
    </div>
</%def>

<h2>Example ${ctx.id}</h2>
<p>for entries</p>
<ul class="inline">
        % for ex in ctx.examples:
           <li>${h.link(request, ex.counterpart.unit)}</li>
        % endfor
</ul>


<blockquote>
    <i>${ctx.name}</i><br/>
    ${ctx.description}
</blockquote>

