execute unless entity @s[tag=rpg.ob.hold] run function rpg:onboard/hold/enter
execute unless entity @s[tag=rpg.ob.queued] run function rpg:onboard/pro/busy
tag @s add rpg.ob.queued
