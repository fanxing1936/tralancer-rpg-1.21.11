execute if score @s rpg_fg_hv = #tv rpg_fg run scoreboard players add @s rpg_fg_hs 1
execute unless score @s rpg_fg_hv = #tv rpg_fg if score @s rpg_fg_hv matches 1.. run function rpg:forge/src/hatred_switch
execute unless score @s rpg_fg_hv = #tv rpg_fg run scoreboard players set @s rpg_fg_hs 1
scoreboard players operation @s rpg_fg_hv = #tv rpg_fg
scoreboard players set @s[scores={rpg_fg_hs=7..}] rpg_fg_hs 6
scoreboard players operation #t rpg_fg = @s rpg_fg_hs
scoreboard players operation #t rpg_fg *= #5 rpg_fg
scoreboard players operation #spct rpg_fg += #t rpg_fg
