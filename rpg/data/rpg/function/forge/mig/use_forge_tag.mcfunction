scoreboard players set #ru rpg_fg 1
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:consumable" set value {consume_seconds:100120f,animation:"eat",sound:"minecraft:entity.generic.eat",has_consume_particles:true,on_consume_effects:[]}
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:food" set value {nutrition:0,saturation:0f,can_always_eat:1b}
