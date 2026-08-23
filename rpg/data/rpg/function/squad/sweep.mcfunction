# 收走没主人的信息板。
#
# 原本用 `distance=..1.5` 判断「附近还有没有佣兵」—— 那是错的：
# 板是**骑**在佣兵身上的，骑乘位比脚下高一截，这个距离量出来够不着，
# 结果板刚生出来就被自己人扫掉，五等佣兵的名牌下方一直是空的。
#
# 改成问它「还骑着东西吗」。骑着就有 vehicle；主人一死，乘客当场被甩下来，
# vehicle 就没了。精确，而且与距离无关。
execute as @e[type=minecraft:text_display,tag=rpg.sq.board] run function rpg:squad/sweep_one
