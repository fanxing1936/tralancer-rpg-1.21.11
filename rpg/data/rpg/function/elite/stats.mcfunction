attribute @s minecraft:max_health modifier add rpg:elite_hp 1.5 add_multiplied_base
attribute @s[tag=rpg.el.boss] minecraft:max_health modifier add rpg:elite_hp2 2.5 add_multiplied_base
attribute @s minecraft:attack_damage modifier add rpg:elite_dmg 0.3 add_multiplied_base
attribute @s[tag=rpg.el.boss] minecraft:attack_damage modifier add rpg:elite_dmg2 0.2 add_multiplied_base
attribute @s minecraft:scale modifier add rpg:elite_scale 0.15 add_multiplied_base
attribute @s[tag=rpg.el.boss] minecraft:scale modifier add rpg:elite_scale2 0.15 add_multiplied_base
data modify entity @s Health set value 2048f
data modify entity @s PersistenceRequired set value 1b
