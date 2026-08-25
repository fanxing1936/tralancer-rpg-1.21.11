clear @s minecraft:paper[minecraft:custom_data~{rpg_ch1_pending_page:1b}]
execute unless entity @s[tag=rpg.name.4] run function rpg:inquest/reveal/4
execute if entity @s[tag=rpg.name.4] unless items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_rite_page:1b,rpg_lord:4}] run function rpg:inquest/give/page4
