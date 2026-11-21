execute if score #lv rpg_fg matches 10.. run scoreboard players set #xp rpg_fg 0
execute if score #lv rpg_fg matches 10.. run return 0
scoreboard players operation #need rpg_fg = #lv rpg_fg
scoreboard players operation #need rpg_fg *= #20 rpg_fg
execute if score #xp rpg_fg < #need rpg_fg run return 0
scoreboard players operation #xp rpg_fg -= #need rpg_fg
scoreboard players add #lv rpg_fg 1
scoreboard players add #up rpg_fg 1
function rpg:forge/xp/loop
