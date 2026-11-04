execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/fail
tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"〖法阵熄灭〗","color":"#C04A3C","bold":true,"italic":false},{"text":" 𝔈𝔵𝔱𝔦𝔫𝔤𝔲𝔦𝔰𝔥𝔢𝔡","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"未能在时限内完成宣判。","color":"#9C9A94","italic":false}]
particle large_smoke ~ ~0.7 ~ 0.7 0.5 0.7 0.08 35 normal
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
function rpg:inquest/tool/cleanup
kill @s
