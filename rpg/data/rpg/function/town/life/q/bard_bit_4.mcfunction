scoreboard players set #b rpg_tl 4
scoreboard players operation #x rpg_tl = @s rpg_tl_bd
scoreboard players operation #x rpg_tl /= #b rpg_tl
scoreboard players operation #x rpg_tl %= #2 rpg_tw
execute if score #x rpg_tl matches 1 run return 0
scoreboard players add @s rpg_tl_bd 4
tellraw @s ["",{"text":"〖","color":"#D9B76A","bold":true,"italic":false},{"text":"吟游诗人","color":"#D9B76A","bold":true,"italic":false},{"text":"〗","color":"#D9B76A","bold":true,"italic":false},{"text":" 𝔅𝔞𝔯𝔡","color":"#8F7430","italic":false},{"text":"  所罗门戴冠走进深渊，七十二个名字带回人间；柱子立着，锁还在，钥匙在教廷的袖子里。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Solomon wore his crown into the deep, and brought back seventy-two names; the pillars stand, the locks still hold, the key is in the Church's sleeve.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.bd03 voice @s ~ ~ ~ 1 1
execute if score @s rpg_tl_bd matches 7 run scoreboard players set @s rpg_tl_q6 8
execute if score @s rpg_tl_bd matches 7 run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  三段都听到了，回去唱给吟游诗人听。","color":"#C9A646","bold":false,"italic":false}]
