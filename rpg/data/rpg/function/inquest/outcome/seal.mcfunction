tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/seal_boss
tellraw @a[distance=..20,gamemode=!spectator] ["",{"text":"〖裁决・封印〗","color":"#4E9FAD","bold":true,"italic":false},{"text":" 𝔖𝔢𝔞𝔩","color":"#336770","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"残魂已收入封魔灯；封印并非永恒。","color":"#9C9A94","italic":false}]
particle soul_fire_flame ~ ~0.8 ~ 1.1 0.6 1.1 0.08 80 force
playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 1.4
function rpg:inquest/tool/cleanup
kill @s
