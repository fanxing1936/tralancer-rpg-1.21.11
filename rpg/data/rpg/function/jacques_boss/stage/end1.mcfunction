# 一阶段打完：变身（火刑柱）。无敌、站定，约 6 秒后进入二阶段。
function rpg:jacques_boss/refill
tag @s add rpg.jqb.morph
scoreboard players set @s rpg_jq_sk 0
scoreboard players set @s rpg_jq_busy 0
scoreboard players set @s rpg_jq_c 0
attribute @s minecraft:armor base set 10
kill @e[tag=rpg.jqb.fx]
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
function rpg:jacques/weapon/glaive
function rpg:jacques/anim/enter/kneel
bossbar set rpg:jacques_boss value 1000
bossbar set rpg:jacques_boss name {"text":"\ue280\ue274\ue270\ue278","font":"rpg:jacques_boss"}
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔫𝔡 𝔐𝔞𝔰𝔱𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……主啊。若这是你的审判，我领受。","color":"#9C9A94","bold":false,"italic":false}]
