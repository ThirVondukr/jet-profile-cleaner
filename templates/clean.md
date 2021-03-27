{{ ctx.message.author.mention }}
{% if response.profile_changed %}
    {% if response.duplicate_items -%}
        Found {{ response.duplicate_items | length }} duplicate items.  
    {%- endif %}
    
    {% if response.removed_orphan_items -%}
        Removed {{ response.removed_orphan_items | length }} orphan items
    {%- endif %}
{% else %}
No duplicate items were found in profile
{% endif %}
