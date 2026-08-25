# 契约之书 —— 由 rpg:item/pact 在长按右键时触发。
#
# `minecraft:using_item` 在按住期间**每刻都会响**，而签约与动用都该是一次性的，
# 所以先用一个短锁去抖：锁没退干净就直接返回。
advancement revoke @s only rpg:item/pact
execute if score @s rpg_lt_divine matches 2 run return run function rpg:divine/borrow
execute if entity @s[scores={rpg_pact_t=1..}] run return 0
scoreboard players set @s rpg_pact_t 8

execute unless entity @s[tag=rpg.pact] run function rpg:pact/sign
execute if entity @s[tag=rpg.pact] run function rpg:pact/invoke
