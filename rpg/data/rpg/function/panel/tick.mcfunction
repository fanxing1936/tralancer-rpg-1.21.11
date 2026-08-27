scoreboard players enable @s rpg_panel
execute if entity @s[tag=rpg.ch1.member] unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run function rpg:campaign/beelzebub/orphan_scrub
execute if entity @s[tag=rpg.ch1.member] if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] unless score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run function rpg:campaign/beelzebub/orphan_scrub
execute if entity @s[tag=rpg.ch1.member] if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] unless score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run function rpg:campaign/beelzebub/orphan_scrub
scoreboard players add @s rpg_panel 0
execute if entity @s[tag=rpg.h.player_tag1,tag=!rpg.panel.open] run function rpg:panel/open
execute unless entity @s[tag=rpg.h.player_tag1] run tag @s remove rpg.panel.open
execute if score @s rpg_panel matches 1 run function rpg:inquest/career
execute if score @s rpg_panel matches 2 run function rpg:panel/inquest
execute if score @s rpg_panel matches 3 run function rpg:panel/pact
execute if score @s rpg_panel matches 4 run function rpg:panel/squad
execute if score @s rpg_panel matches 5 run function rpg:panel/hud_toggle
execute if score @s rpg_panel matches 6 run function rpg:panel/help
execute if score @s rpg_panel matches 7 run function rpg:panel/endless
execute if score @s rpg_panel matches 8 run function rpg:panel/open
execute if score @s rpg_panel matches 9 run function rpg:divine/judgment/arm
execute if score @s rpg_panel matches 10 run function rpg:divine/gift
execute if score @s rpg_panel matches 11 run function rpg:campaign/beelzebub/menu
execute if score @s rpg_panel matches 12 run function rpg:campaign/beelzebub/start
execute if score @s rpg_panel matches 13 run function rpg:campaign/beelzebub/rescue
execute if score @s rpg_panel matches 14 run function rpg:campaign/beelzebub/join
execute if score @s rpg_panel matches 15 run function rpg:campaign/beelzebub/next_hunt
execute if score @s rpg_panel matches 16 run function rpg:endless/start
execute if score @s rpg_panel matches 17 run function rpg:endless/join
execute if score @s rpg_panel matches 18 run function rpg:prayer/menu
execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0
