scoreboard players set @s rpg_jq_sk 8
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 30
data merge entity @s {NoAI:1b}
function rpg:jacques/anim/enter/horn
function rpg:jacques/weapon/none
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣殿号角 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"圣殿的弟兄们，列阵！","color":"#9C9A94","bold":false,"italic":false}]
