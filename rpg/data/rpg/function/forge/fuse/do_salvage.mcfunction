# 拆解（as/at 玩家）
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"主手要拿着魂火冶炼出来的装备","color":"#FF6B5E","bold":false,"italic":false}]
data modify storage rpg:forge sv set from entity @s SelectedItem.components."minecraft:custom_data".rpg_eq
execute if data storage rpg:forge sv{rune:"backstab"} run loot give @s loot rpg:forge/item/rune_backstab
execute if data storage rpg:forge sv{rune:"bloodpact"} run loot give @s loot rpg:forge/item/rune_bloodpact
execute if data storage rpg:forge sv{rune:"echo"} run loot give @s loot rpg:forge/item/rune_echo
execute if data storage rpg:forge sv{rune:"ember"} run loot give @s loot rpg:forge/item/rune_ember
execute if data storage rpg:forge sv{rune:"execute"} run loot give @s loot rpg:forge/item/rune_execute
execute if data storage rpg:forge sv{rune:"hunt"} run loot give @s loot rpg:forge/item/rune_hunt
execute if data storage rpg:forge sv{rune:"lastbreath"} run loot give @s loot rpg:forge/item/rune_lastbreath
execute if data storage rpg:forge sv{rune:"meteor"} run loot give @s loot rpg:forge/item/rune_meteor
execute if data storage rpg:forge sv{rune:"poise"} run loot give @s loot rpg:forge/item/rune_poise
execute if data storage rpg:forge sv{rune:"recoil"} run loot give @s loot rpg:forge/item/rune_recoil
execute if data storage rpg:forge sv{rune:"split"} run loot give @s loot rpg:forge/item/rune_split
execute if data storage rpg:forge sv{rune:"stillwater"} run loot give @s loot rpg:forge/item/rune_stillwater
execute if data storage rpg:forge sv{rune:"swift"} run loot give @s loot rpg:forge/item/rune_swift
execute if data storage rpg:forge sv{stone:"banner"} run loot give @s loot rpg:forge/item/stone_banner
execute if data storage rpg:forge sv{stone:"blood"} run loot give @s loot rpg:forge/item/stone_blood
execute if data storage rpg:forge sv{stone:"frost"} run loot give @s loot rpg:forge/item/stone_frost
execute if data storage rpg:forge sv{stone:"gale"} run loot give @s loot rpg:forge/item/stone_gale
execute if data storage rpg:forge sv{stone:"rift"} run loot give @s loot rpg:forge/item/stone_rift
execute if data storage rpg:forge sv{stone:"shadow"} run loot give @s loot rpg:forge/item/stone_shadow
execute if data storage rpg:forge sv{stone:"volley"} run loot give @s loot rpg:forge/item/stone_volley
execute if data storage rpg:forge sv{src:"faith"} run loot give @s loot rpg:forge/item/source_faith
execute if data storage rpg:forge sv{src:"hatred"} run loot give @s loot rpg:forge/item/source_hatred
execute if data storage rpg:forge sv{src:"hope"} run loot give @s loot rpg:forge/item/source_hope
execute if data storage rpg:forge sv{src:"malice"} run loot give @s loot rpg:forge/item/source_malice
execute if data storage rpg:forge sv{src:"pride"} run loot give @s loot rpg:forge/item/source_pride
execute if data storage rpg:forge sv{src:"resolve"} run loot give @s loot rpg:forge/item/source_resolve
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] unless items entity @s weapon.mainhand #rpg:fuse/rich run give @s minecraft:iron_ingot 3
execute if items entity @s weapon.mainhand #rpg:fuse/rich run give @s minecraft:diamond 2
loot give @s loot rpg:forge/item/soul
item replace entity @s weapon.mainhand with minecraft:air
scoreboard players add @s rpg_tl_fu 1
particle minecraft:smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 20
playsound minecraft:block.grindstone.use player @a[distance=..16] ~ ~ ~ 1 0.9
tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"拆解完成：材料与镶嵌的东西都退回来了","color":"#C9A646","bold":false,"italic":false}]
