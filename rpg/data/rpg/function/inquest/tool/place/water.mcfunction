scoreboard players add @s rpg_rite_id 0
summon minecraft:item_display ~0.65 ~0.06 ~-0.85 {Tags:["rpg.rite.prop","rpg.rite.prop.new","rpg.rite.prop.water"],item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:enchantment_glint_override":1b,"minecraft:potion_contents":{custom_color:16773320}}},item_display:"ground",view_range:0.65f,shadow_radius:0.18f,shadow_strength:0.45f,brightness:{block:15,sky:12},transformation:{translation:[0f,0.03f,0f],scale:[0.76f,0.76f,0.76f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3,sort=nearest,limit=1] rpg_rite_id = @s rpg_rite_id
scoreboard players set @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3,sort=nearest,limit=1] rpg_prop_t 200
tag @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3] remove rpg.rite.prop.new
