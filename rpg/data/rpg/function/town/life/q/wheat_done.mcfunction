tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"村长","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔉𝔞𝔯𝔪𝔢𝔯","color":"#8F7430","italic":false},{"text":"  苍蝇。成团成团的。冬天哪来的苍蝇。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Flies. Swarms of them. Where do flies come from at this time of year?","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.rb02 voice @s ~ ~ ~ 1 1
give @s minecraft:bread[minecraft:custom_name=["",{"text":"[城镇]","color":"#C9A646","bold":true,"italic":false},{"text":"黑麦面包","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false},{"text":"教堂分给每户的口粮","color":"gray","bold":false,"italic":false},{"text":"路上饿了就掰一块","color":"gray","bold":false,"italic":false},{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false}],minecraft:custom_data={rpg_food:"rye_bread"},minecraft:item_model="rpg:town/rye_bread"] 12
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
scoreboard players set @s rpg_tl_q4 0
scoreboard players operation @s rpg_tl_qd4 = #day1 rpg_tl
function rpg:town/life/rep_add {n:10}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  发黑的麦子","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
