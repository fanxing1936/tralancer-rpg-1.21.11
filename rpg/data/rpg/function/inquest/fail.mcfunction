tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖仪式失败〗","color":"#C04A3C","bold":true,"italic":false},{"text":" ℜ𝔦𝔱𝔢 𝔅𝔯𝔬𝔨𝔢𝔫","color":"#7D3027","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"法阵失去约束，裁决被迫进入消灭步骤。","color":"#9C9A94","italic":false}]
function rpg:inquest/outcome/eliminate_boss
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
