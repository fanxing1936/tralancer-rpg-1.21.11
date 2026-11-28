# 每日口粮：每个现实日一次；原质第 3 阶以前多给一份材料；声望 20 再加一份
execute if score @s rpg_tl_d = #day1 rpg_tl run return run function rpg:town/life/ration_no
scoreboard players operation @s rpg_tl_d = #day1 rpg_tl
tellraw @s ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  今天的口粮。别空着肚子出门。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Today's ration. Don't go out on an empty stomach.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr05 voice @s ~ ~ ~ 1 1
give @s minecraft:bread[minecraft:custom_name=["",{"text":"[城镇]","color":"#C9A646","bold":true,"italic":false},{"text":"黑麦面包","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false},{"text":"教堂分给每户的口粮","color":"gray","bold":false,"italic":false},{"text":"路上饿了就掰一块","color":"gray","bold":false,"italic":false},{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false}],minecraft:custom_data={rpg_food:"rye_bread"},minecraft:item_model="rpg:town/rye_bread"] 8
loot give @s loot rpg:potion/blood
execute unless score @s rpg_sef matches 3.. run loot give @s loot rpg:forge/item/soul
execute unless score @s rpg_sef matches 3.. run loot give @s loot rpg:forge/item/blank
function rpg:town/life/rep_get
execute if score #rep rpg_tl matches 20.. run give @s minecraft:cooked_beef[minecraft:custom_name=["",{"text":"[城镇]","color":"#C9A646","bold":true,"italic":false},{"text":"腌熏肉","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false},{"text":"熏房里挂了一冬的肉","color":"gray","bold":false,"italic":false},{"text":"比面包顶饿","color":"gray","bold":false,"italic":false},{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false}],minecraft:custom_data={rpg_food:"smoked_meat"},minecraft:item_model="rpg:town/smoked_meat"] 6
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 1
