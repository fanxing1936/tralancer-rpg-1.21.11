execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_rite_id run return run function rpg:campaign/beelzebub/verdict/eliminate
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/eliminate_boss
particle explosion ~ ~0.7 ~ 0.4 0.3 0.4 0.04 3 force
playsound minecraft:entity.wither.spawn hostile @a[distance=..32] ~ ~ ~ 0.8 1.25
function rpg:inquest/tool/cleanup
kill @s
