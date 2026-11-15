scoreboard players set @s rpg_ub_sk 1
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 40
function rpg:usurper/anim/enter/attack
playsound rpg:usurper.prepare hostile @a[distance=..32] ~ ~ ~ 1 1
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"所罗门封印 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"跪进所罗门的封印里。","color":"#9C9A94","bold":false,"italic":false}]
execute at @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=2] run function rpg:usurper_boss/seal/place
