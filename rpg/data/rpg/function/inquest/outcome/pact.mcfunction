tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/pact_boss
tellraw @a[distance=..20,gamemode=!spectator] ["",{"text":"[裁决·契约] ","color":"#D596F2","bold":true,"italic":false},{"text":"恶魔以柱之书留下力量；接受者增加 25 魔化。","color":"gray","italic":false}]
particle sculk_charge_pop ~ ~0.8 ~ 1.1 0.7 1.1 0.1 90 force
playsound minecraft:block.end_portal.spawn hostile @a[distance=..28] ~ ~ ~ 0.8 0.6
function rpg:inquest/tool/cleanup
kill @s
