# 契约之书 —— 由 rpg:item/pact 在长按右键时触发。
#
# `minecraft:using_item` 在按住期间**每刻都会响**，而签约与动用都该是一次性的，
# 所以先用一个短锁去抖：锁没退干净就直接返回。
advancement revoke @s only rpg:item/pact
execute if score @s rpg_lt_divine matches 2 run return run function rpg:divine/borrow
# 对话框开着时客户端仍算在长按，这里要一直顶住锁，否则界面每隔一会儿就重开一次。
execute if entity @s[tag=rpg.pact.ui] run scoreboard players set @s rpg_pact_t 8
execute if entity @s[scores={rpg_pact_t=1..}] run return 0
scoreboard players set @s rpg_pact_t 8

# 书放副手也能用：主手没有契约书，就认副手那一本。
tag @s remove rpg.pact.off
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact_tag:1b}] run tag @s add rpg.pact.off

execute unless entity @s[tag=rpg.pact] run function rpg:pact/sign
execute if entity @s[tag=rpg.pact] run function rpg:pact/invoke
