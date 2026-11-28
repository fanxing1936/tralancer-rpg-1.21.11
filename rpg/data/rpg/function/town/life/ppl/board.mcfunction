summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tnpc","rpg.tnpc.board","rpg.tl.new"],width:1.4f,height:2.2f,response:1b}
setblock ~ ~ ~ minecraft:lectern[facing=north]
summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.tnpc.plate"],billboard:"center",text:["",{"text":"告示板","color":"#E6DFCF","bold":true,"italic":false},{"text":"\n𝔑𝔬𝔱𝔦𝔠𝔢 𝔅𝔬𝔞𝔯𝔡","color":"#8F7430","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:interaction,tag=rpg.tl.new] rpg_tw_id = #built rpg_tw
tag @e[tag=rpg.tl.new] remove rpg.tl.new
