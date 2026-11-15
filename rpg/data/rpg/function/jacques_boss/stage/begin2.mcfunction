tag @s remove rpg.jqb.morph
tag @s remove rpg.jqb.u1
tag @s remove rpg.jqb.u2
tag @s remove rpg.jqb.last1
data merge entity @s {NoAI:0b,Invulnerable:0b}
scoreboard players set @s rpg_jq 2
scoreboard players set #stage rpg_jq 2
scoreboard players set @s rpg_jq_c 0
scoreboard players set @s rpg_jq_n 0
scoreboard players set @s rpg_jq_k 0
scoreboard players set @s rpg_jq_cb 0
scoreboard players set @s rpg_jq_b 20
scoreboard players set @s rpg_jq_sk 0
bossbar set rpg:jacques_boss name {"text":"\ue2b4\ue275\ue271\ue279","font":"rpg:jacques_boss"}
scoreboard players set @s rpg_jq_s 20
function rpg:jacques_boss/music/2
particle minecraft:flash{color:16747069} ~ ~1.5 ~ 0 0 0 0 1 force
playsound minecraft:item.firecharge.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔅𝔲𝔯𝔫𝔦𝔫𝔤 𝔒𝔞𝔱𝔥","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第二阶段 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"他们把我送上了火刑柱。可我还站着。","color":"#9C9A94","bold":false,"italic":false}]
