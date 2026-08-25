tag @s add rpg.ch1.ui.title.8
execute if score @s rpg_ch1_choice matches 1 run function rpg:campaign/beelzebub/ui/title/verdict_eliminate
execute if score @s rpg_ch1_choice matches 2 run function rpg:campaign/beelzebub/ui/title/verdict_banish
execute if score @s rpg_ch1_choice matches 3 run function rpg:campaign/beelzebub/ui/title/verdict_seal
execute if score @s rpg_ch1_choice matches 4 run function rpg:campaign/beelzebub/ui/title/verdict_pact
