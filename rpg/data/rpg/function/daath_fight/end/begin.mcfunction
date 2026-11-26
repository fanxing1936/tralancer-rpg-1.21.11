tag @s add rpg.dt.end
tag @s remove rpg.dt.window
scoreboard players set @s rpg_dt_t 0
scoreboard players set @s rpg_dt_q 0
data merge entity @s {NoAI:1b,Invulnerable:1b}
function rpg:daath_fight/weapon/none
function rpg:daath_fight/bar/zero
kill @e[tag=rpg.dt.fx,distance=..60]
function rpg:daath/anim/enter/kneel
stopsound @a[tag=rpg.dt.me,limit=1] record
summon minecraft:interaction ~ ~ ~ {Tags:["rpg.dt.touch"],width:1.6f,height:2.4f,response:1b}
execute as @a[tag=rpg.dt.me,limit=1] run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"它跪下了。攻击它，","color":"#AAB4C3","bold":false,"italic":false},{"text":"斩断","color":"#FF5A62","bold":true,"italic":false},{"text":"；空手右键，","color":"#AAB4C3","bold":false,"italic":false},{"text":"接纳","color":"#62B8F0","bold":true,"italic":false},{"text":"。","color":"#AAB4C3","bold":false,"italic":false}]
