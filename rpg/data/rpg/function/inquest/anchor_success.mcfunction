execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_success
particle explosion ~ ~0.7 ~ 0.3 0.25 0.3 0 2 force
particle end_rod ~ ~0.8 ~ 1.3 0.8 1.3 0.14 100 force
playsound minecraft:block.beacon.deactivate player @a[distance=..24] ~ ~ ~ 1 1.7
function rpg:inquest/tool/cleanup
kill @s
