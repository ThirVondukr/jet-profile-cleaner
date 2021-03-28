{{ ctx.message.author.mention }}
{% if response.profile_changed %}
    {% if response.duplicate_items -%}
        Removed {{ response.duplicate_items | length }} duplicate item(s).  
    {%- endif %}
    
    {% if response.removed_orphan_items -%}
        Removed {{ response.removed_orphan_items | length }} orphan item(s).
    {%- endif %}
{% else %}
No duplicate items were found in profile
{% endif %}
