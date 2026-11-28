scoreboard players set #b rpg_tl 1
scoreboard players operation #x rpg_tl = @s rpg_tl_bd
scoreboard players operation #x rpg_tl /= #b rpg_tl
scoreboard players operation #x rpg_tl %= #2 rpg_tw
execute if score #x rpg_tl matches 1 run return 0
scoreboard players add @s rpg_tl_bd 1
tellraw @s ["",{"text":"〖","color":"#D9B76A","bold":true,"italic":false},{"text":"吟游诗人","color":"#D9B76A","bold":true,"italic":false},{"text":"〗","color":"#D9B76A","bold":true,"italic":false},{"text":" 𝔅𝔞𝔯𝔡","color":"#8F7430","italic":false},{"text":"  世界曾是一整块，神说要有光；后来权与力分了家，大地就碎成了七样。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"The world was whole when God said light; then Might and Authority parted, and the land broke into seven.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.bd01 voice @s ~ ~ ~ 1 1
execute if score @s rpg_tl_bd matches 7 run scoreboard players set @s rpg_tl_q6 8
execute if score @s rpg_tl_bd matches 7 run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  三段都听到了，回去唱给吟游诗人听。","color":"#C9A646","bold":false,"italic":false}]
