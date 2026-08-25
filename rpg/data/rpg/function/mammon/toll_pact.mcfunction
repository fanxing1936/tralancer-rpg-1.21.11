# 第七柱的人：贪婪不从他口袋里掏，它从魂上收。
# 柱位的枷锁本来就是「魔化沾染速度翻倍」，这一条接在同一根线上。
scoreboard players add @s rpg_taint 2
function rpg:hud/m30
playsound minecraft:block.sculk.charge player @s ~ ~ ~ 0.8 0.6
execute at @s run particle sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.02 8
