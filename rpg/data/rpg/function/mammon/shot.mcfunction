# 这一箭是玛门的。@s 是那支原箭。
#
# 买断与否，先在这里定下来：射手攒够了刻数，这一发就是买来的。
scoreboard players set #gold rpg_mam 0
execute on origin if entity @s[scores={rpg_mam_c=40..}] run scoreboard players set #gold rpg_mam 1

# 三根箭共用的底子：归属、伤害、以及**发射它的那把弓**都跟着原箭走。
#
# 伤害不写死：箭的 damage 是基数，命中伤害是它乘以飞行速度、再叠附魔。
# 照抄原箭，附赠的两根才和真箭一模一样 —— 这才叫「一次射出三根」。
# weapon 是 1.21.5 之后箭身上记的那把弓，力量／冲击／火矢都由它生效；
# 先 remove 再 set from：万一原箭没有这一项，storage 里不该留着上一发的。
data modify storage rpg:mam owner set from entity @s Owner
data modify storage rpg:mam dmg set from entity @s damage
data remove storage rpg:mam weapon
data modify storage rpg:mam weapon set from entity @s weapon
data modify storage rpg:mam pierce set value 0b
execute if score #gold rpg_mam matches 1 run data modify storage rpg:mam dmg set value 4.0d
execute if score #gold rpg_mam matches 1 run data modify storage rpg:mam pierce set value 5b
execute if score #gold rpg_mam matches 1 run function rpg:mammon/gild

# 原箭的速度。附赠的两根在这个基础上各抖一下 —— 三角函数在命令里太贵，
# 而定速矢量上的小扰动本来就等价于一个小角度的偏转。
execute store result score #mx rpg_mam run data get entity @s Motion[0] 1000
execute store result score #my rpg_mam run data get entity @s Motion[1] 1000
execute store result score #mz rpg_mam run data get entity @s Motion[2] 1000
function rpg:mammon/fork
function rpg:mammon/fork

# 结算记在射手头上
execute on origin run function rpg:mammon/settle
