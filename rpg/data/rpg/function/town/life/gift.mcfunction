# 报到：新手大礼包（一辈子一次）
execute if score @s rpg_tl_gift matches 1.. run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  新人的那份你已经领过了。每天来领口粮吧。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_tl_gift 1
tellraw @s ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  孩子，你醒了。这里是你的故乡，你在这里出生，也在这里受洗。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"You're awake, child. This is your home; you were born here, and baptised here.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr01 voice @s ~ ~ ~ 1 1
scoreboard players add #sid rpg_say 1
scoreboard players operation @s rpg_say = #sid rpg_say
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 131
function rpg:town/say/push {f:14}
give @s minecraft:bread[minecraft:custom_name=["",{"text":"[城镇]","color":"#C9A646","bold":true,"italic":false},{"text":"黑麦面包","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false},{"text":"教堂分给每户的口粮","color":"gray","bold":false,"italic":false},{"text":"路上饿了就掰一块","color":"gray","bold":false,"italic":false},{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false}],minecraft:custom_data={rpg_food:"rye_bread"},minecraft:item_model="rpg:town/rye_bread"] 16
give @s minecraft:cooked_beef[minecraft:custom_name=["",{"text":"[城镇]","color":"#C9A646","bold":true,"italic":false},{"text":"腌熏肉","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false},{"text":"熏房里挂了一冬的肉","color":"gray","bold":false,"italic":false},{"text":"比面包顶饿","color":"gray","bold":false,"italic":false},{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false}],minecraft:custom_data={rpg_food:"smoked_meat"},minecraft:item_model="rpg:town/smoked_meat"] 8
loot give @s loot rpg:potion/blood
loot give @s loot rpg:potion/blood
function rpg:alc/give/holy
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/forge_stone
give @s minecraft:paper[minecraft:custom_name=["",{"text":"[城镇]","color":"#C9A646","bold":true,"italic":false},{"text":"余烬归途","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false},{"text":"手持右键，站着念 5 秒，回到故乡","color":"gray","bold":false,"italic":false},{"text":"挨打或走动会打断","color":"gray","bold":false,"italic":false},{"text":"+------------------+","color":"#FFFFFF","bold":false,"italic":false}],minecraft:custom_data={rpg_home:1b},minecraft:item_model="rpg:town/home_scroll",minecraft:consumable={consume_seconds:1234567.0f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false},minecraft:max_stack_size=16] 2
execute unless entity @s[tag=rpg.tl.holy] unless score @s rpg_tl_born matches 1.. run function rpg:town/life/holy_start
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 269
function rpg:town/say/push {f:13}
execute store result score #r rpg_tl run scoreboard players get @s rpg_tl_t
scoreboard players operation @s rpg_tl_d = #day1 rpg_tl
function rpg:town/life/rep_add {n:5}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.2
