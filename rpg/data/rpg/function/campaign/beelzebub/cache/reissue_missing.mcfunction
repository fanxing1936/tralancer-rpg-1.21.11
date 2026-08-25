execute if entity @s[tag=rpg.ch1.kit.issued] run return 0
tag @s add rpg.ch1.kit.issued
execute unless items entity @s inventory.* minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] run function rpg:campaign/beelzebub/give/totem
execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_ch1_pending_page:1b}] unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,limit=1] run function rpg:campaign/beelzebub/give/pending_page
execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_medium:4b}] run function rpg:inquest/give/medium4
execute unless items entity @s inventory.* minecraft:lingering_potion[minecraft:custom_data~{rpg_strong_water:1b}] run function rpg:inquest/give/strong_water
execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_nail:1b}] run function rpg:inquest/give/nail
execute unless items entity @s inventory.* minecraft:goat_horn[minecraft:custom_data~{rpg_bell:1b}] run function rpg:inquest/give/bell
execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_incense:1b}] run function rpg:inquest/give/incense
execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_chalk:1b}] run function rpg:inquest/give/chalk1
execute unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] run function rpg:inquest/give/lantern
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,tag=rpg.ch1.witness.ready,limit=1] run function rpg:campaign/beelzebub/witness/confirm_player
