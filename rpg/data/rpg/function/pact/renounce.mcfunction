# 毁约。
#
# 契约本来只有逆圣化一条出路，而逆圣化要求魔化先推到 100 ——
# 对签错柱位的人那不是出路，是死胡同。所以给它第二条：
# 借驱魔仪式的火烧断它。仪式本来就是烧污染的，成本也实打实
# （一支图腾加一瓶圣水）。
#
# 顺序要紧：先把书退回未立约，再 break —— break 会清掉柱位编号，
# 清掉之后就认不出该退成哪一本了。
execute if entity @s[scores={rpg_pact=1}] run function rpg:pact/unsign1
execute if entity @s[scores={rpg_pact=2}] run function rpg:pact/unsign2
execute if entity @s[scores={rpg_pact=3}] run function rpg:pact/unsign3
execute if entity @s[scores={rpg_pact=4}] run function rpg:pact/unsign4
execute if entity @s[scores={rpg_pact=5}] run function rpg:pact/unsign5
execute if entity @s[scores={rpg_pact=6}] run function rpg:pact/unsign6
execute if entity @s[scores={rpg_pact=7}] run function rpg:pact/unsign7
function rpg:pact/break

# 柱中的东西不会白白松手。
scoreboard players add @s rpg_taint 20
execute if entity @s[scores={rpg_taint=101..}] run scoreboard players set @s rpg_taint 100
effect give @s minecraft:wither 10 1
effect give @s minecraft:blindness 4 0

particle minecraft:flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~1 ~ 0.6 0.8 0.6 0.25 120
particle sculk_charge_pop ~ ~1 ~ 0.5 0.7 0.5 0.12 80
playsound minecraft:block.beacon.deactivate master @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:entity.wither.hurt master @s ~ ~ ~ 1 0.7
title @s times 10 60 20
title @s title ["",{"text":"契 约 已 断","italic":false,"color":"gold","bold":true}]
title @s subtitle ["",{"text":"柱位空了出来，代价留在你身上","italic":false,"color":"gray"}]

# 图腾把自己烧尽了
kill @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..6,limit=1,sort=nearest]
