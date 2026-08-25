$execute if entity @a[tag=rpg.divine.cast,limit=1] run damage @s $(amount) rpg:divine_light by @a[tag=rpg.divine.cast,limit=1,sort=nearest]
$execute unless entity @a[tag=rpg.divine.cast,limit=1] run damage @s $(amount) rpg:divine_light
