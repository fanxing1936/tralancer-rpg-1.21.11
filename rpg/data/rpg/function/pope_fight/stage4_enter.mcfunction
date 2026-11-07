# Boss 二阶段：末影之心升起，教皇困在体内。
scoreboard players set #stage rpg_pf 4
scoreboard players set #t rpg_pf 0
function rpg:pope_fight/bgm/play_3
bossbar set minecraft:pope name {"text":"","font":"rpg:pope_fx"}
scoreboard players set #hudl rpg_pf 20
bossbar set minecraft:pope max 1000
bossbar set minecraft:pope value 1000
particle dust{color:[0.835f,0.588f,0.949f],scale:1.6} ~ ~1 ~ 1.5 0.5 1.5 0.1 64 force
particle flash{color:13997810} ~ ~1 ~ 0 0 0 0 1 force
tellraw @a[distance=..48] ["",{"text":"〖末影之心〗","color":"#A276BE","bold":true,"italic":false},{"text":" ℌ𝔢𝔞𝔯𝔱 𝔬𝔣 𝔈𝔫𝔡𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣力……从来就不是圣的。","color":"#9C9A94","bold":false,"italic":false}]
execute positioned over motion_blocking_no_leaves run function rpg:pope_fight/heart/spawn
