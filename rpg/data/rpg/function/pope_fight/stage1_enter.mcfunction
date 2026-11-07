# 第一阶段：圣卫降临，教皇不在场。
scoreboard players set #stage rpg_pf 1
scoreboard players set #t rpg_pf 0
function rpg:pope_fight/bgm/play_1
bossbar set minecraft:pope name {"text":"","font":"rpg:pope_fx"}
bossbar set minecraft:pope max 4
bossbar set minecraft:pope value 4
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔓𝔬𝔭𝔢","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣座已宣告：你是异端。","color":"#9C9A94","bold":false,"italic":false}]
execute positioned ~6 ~ ~0 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute positioned ~-6 ~ ~0 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute positioned ~0 ~ ~6 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute positioned ~0 ~ ~-6 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
