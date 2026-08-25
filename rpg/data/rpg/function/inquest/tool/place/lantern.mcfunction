scoreboard players add @s rpg_rite_id 0
summon minecraft:item_display ~0.95 ~0.06 ~1.05 {Tags:["rpg.rite.prop","rpg.rite.prop.new","rpg.rite.prop.lantern","rpg.rite.prop.linger"],item:{id:"minecraft:soul_lantern",count:1,components:{"minecraft:enchantment_glint_override":1b}},item_display:"ground",view_range:0.65f,shadow_radius:0.18f,shadow_strength:0.45f,brightness:{block:15,sky:12},transformation:{translation:[0f,0.03f,0f],scale:[0.92f,0.92f,0.92f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3,sort=nearest,limit=1] rpg_rite_id = @s rpg_rite_id
scoreboard players set @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3,sort=nearest,limit=1] rpg_prop_t 120
tag @e[type=minecraft:item_display,tag=rpg.rite.prop.new,distance=..3] remove rpg.rite.prop.new
