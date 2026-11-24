# 技能页数据（as 玩家）→ storage rpg:force p
data modify storage rpg:force p set value {}
scoreboard players add @s rpg_sp 0
execute store result storage rpg:force p.sp int 1 run scoreboard players get @s rpg_sp
scoreboard players add @s rpg_k01 0
execute store result storage rpg:force p.l01 int 1 run scoreboard players get @s rpg_k01
data modify storage rpg:force p.c01 set value "#5A5852"
execute if score @s rpg_force matches 1 run data modify storage rpg:force p.c01 set value "#E6DFCF"
execute if score @s rpg_force matches 3 run data modify storage rpg:force p.c01 set value "#E6DFCF"
execute if score @s rpg_k01 matches 1.. run data modify storage rpg:force p.c01 set value "#FFD85A"
scoreboard players add @s rpg_k02 0
execute store result storage rpg:force p.l02 int 1 run scoreboard players get @s rpg_k02
data modify storage rpg:force p.c02 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k01 matches 1.. run data modify storage rpg:force p.c02 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k01 matches 1.. run data modify storage rpg:force p.c02 set value "#E6DFCF"
execute if score @s rpg_k02 matches 1.. run data modify storage rpg:force p.c02 set value "#FFD85A"
scoreboard players add @s rpg_k03 0
execute store result storage rpg:force p.l03 int 1 run scoreboard players get @s rpg_k03
data modify storage rpg:force p.c03 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k02 matches 1.. run data modify storage rpg:force p.c03 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k02 matches 1.. run data modify storage rpg:force p.c03 set value "#E6DFCF"
execute if score @s rpg_k03 matches 1.. run data modify storage rpg:force p.c03 set value "#FFD85A"
scoreboard players add @s rpg_k04 0
execute store result storage rpg:force p.l04 int 1 run scoreboard players get @s rpg_k04
data modify storage rpg:force p.c04 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k03 matches 1.. run data modify storage rpg:force p.c04 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k03 matches 1.. run data modify storage rpg:force p.c04 set value "#E6DFCF"
execute if score @s rpg_k04 matches 1.. run data modify storage rpg:force p.c04 set value "#FFD85A"
scoreboard players add @s rpg_k05 0
execute store result storage rpg:force p.l05 int 1 run scoreboard players get @s rpg_k05
data modify storage rpg:force p.c05 set value "#5A5852"
execute if score @s rpg_force matches 1 run data modify storage rpg:force p.c05 set value "#E6DFCF"
execute if score @s rpg_force matches 3 run data modify storage rpg:force p.c05 set value "#E6DFCF"
execute if score @s rpg_k05 matches 1.. run data modify storage rpg:force p.c05 set value "#FFD85A"
scoreboard players add @s rpg_k06 0
execute store result storage rpg:force p.l06 int 1 run scoreboard players get @s rpg_k06
data modify storage rpg:force p.c06 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k05 matches 1.. run data modify storage rpg:force p.c06 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k05 matches 1.. run data modify storage rpg:force p.c06 set value "#E6DFCF"
execute if score @s rpg_k06 matches 1.. run data modify storage rpg:force p.c06 set value "#FFD85A"
scoreboard players add @s rpg_k07 0
execute store result storage rpg:force p.l07 int 1 run scoreboard players get @s rpg_k07
data modify storage rpg:force p.c07 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k06 matches 1.. run data modify storage rpg:force p.c07 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k06 matches 1.. run data modify storage rpg:force p.c07 set value "#E6DFCF"
execute if score @s rpg_k07 matches 1.. run data modify storage rpg:force p.c07 set value "#FFD85A"
scoreboard players add @s rpg_k08 0
execute store result storage rpg:force p.l08 int 1 run scoreboard players get @s rpg_k08
data modify storage rpg:force p.c08 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k07 matches 1.. run data modify storage rpg:force p.c08 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k07 matches 1.. run data modify storage rpg:force p.c08 set value "#E6DFCF"
execute if score @s rpg_k08 matches 1.. run data modify storage rpg:force p.c08 set value "#FFD85A"
scoreboard players add @s rpg_k09 0
execute store result storage rpg:force p.l09 int 1 run scoreboard players get @s rpg_k09
data modify storage rpg:force p.c09 set value "#5A5852"
execute if score @s rpg_force matches 1 run data modify storage rpg:force p.c09 set value "#E6DFCF"
execute if score @s rpg_force matches 3 run data modify storage rpg:force p.c09 set value "#E6DFCF"
execute if score @s rpg_k09 matches 1.. run data modify storage rpg:force p.c09 set value "#FFD85A"
scoreboard players add @s rpg_k10 0
execute store result storage rpg:force p.l10 int 1 run scoreboard players get @s rpg_k10
data modify storage rpg:force p.c10 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k09 matches 1.. run data modify storage rpg:force p.c10 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k09 matches 1.. run data modify storage rpg:force p.c10 set value "#E6DFCF"
execute if score @s rpg_k10 matches 1.. run data modify storage rpg:force p.c10 set value "#FFD85A"
scoreboard players add @s rpg_k11 0
execute store result storage rpg:force p.l11 int 1 run scoreboard players get @s rpg_k11
data modify storage rpg:force p.c11 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k10 matches 1.. run data modify storage rpg:force p.c11 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k10 matches 1.. run data modify storage rpg:force p.c11 set value "#E6DFCF"
execute if score @s rpg_k11 matches 1.. run data modify storage rpg:force p.c11 set value "#FFD85A"
scoreboard players add @s rpg_k12 0
execute store result storage rpg:force p.l12 int 1 run scoreboard players get @s rpg_k12
data modify storage rpg:force p.c12 set value "#5A5852"
execute if score @s rpg_force matches 1 if score @s rpg_k11 matches 1.. run data modify storage rpg:force p.c12 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k11 matches 1.. run data modify storage rpg:force p.c12 set value "#E6DFCF"
execute if score @s rpg_k12 matches 1.. run data modify storage rpg:force p.c12 set value "#FFD85A"
scoreboard players add @s rpg_k13 0
execute store result storage rpg:force p.l13 int 1 run scoreboard players get @s rpg_k13
data modify storage rpg:force p.c13 set value "#5A5852"
execute if score @s rpg_force matches 2 run data modify storage rpg:force p.c13 set value "#E6DFCF"
execute if score @s rpg_force matches 3 run data modify storage rpg:force p.c13 set value "#E6DFCF"
execute if score @s rpg_k13 matches 1.. run data modify storage rpg:force p.c13 set value "#A276BE"
scoreboard players add @s rpg_k14 0
execute store result storage rpg:force p.l14 int 1 run scoreboard players get @s rpg_k14
data modify storage rpg:force p.c14 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k13 matches 1.. run data modify storage rpg:force p.c14 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k13 matches 1.. run data modify storage rpg:force p.c14 set value "#E6DFCF"
execute if score @s rpg_k14 matches 1.. run data modify storage rpg:force p.c14 set value "#A276BE"
scoreboard players add @s rpg_k15 0
execute store result storage rpg:force p.l15 int 1 run scoreboard players get @s rpg_k15
data modify storage rpg:force p.c15 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k14 matches 1.. run data modify storage rpg:force p.c15 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k14 matches 1.. run data modify storage rpg:force p.c15 set value "#E6DFCF"
execute if score @s rpg_k15 matches 1.. run data modify storage rpg:force p.c15 set value "#A276BE"
scoreboard players add @s rpg_k16 0
execute store result storage rpg:force p.l16 int 1 run scoreboard players get @s rpg_k16
data modify storage rpg:force p.c16 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k15 matches 1.. run data modify storage rpg:force p.c16 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k15 matches 1.. run data modify storage rpg:force p.c16 set value "#E6DFCF"
execute if score @s rpg_k16 matches 1.. run data modify storage rpg:force p.c16 set value "#A276BE"
scoreboard players add @s rpg_k17 0
execute store result storage rpg:force p.l17 int 1 run scoreboard players get @s rpg_k17
data modify storage rpg:force p.c17 set value "#5A5852"
execute if score @s rpg_force matches 2 run data modify storage rpg:force p.c17 set value "#E6DFCF"
execute if score @s rpg_force matches 3 run data modify storage rpg:force p.c17 set value "#E6DFCF"
execute if score @s rpg_k17 matches 1.. run data modify storage rpg:force p.c17 set value "#A276BE"
scoreboard players add @s rpg_k18 0
execute store result storage rpg:force p.l18 int 1 run scoreboard players get @s rpg_k18
data modify storage rpg:force p.c18 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k17 matches 1.. run data modify storage rpg:force p.c18 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k17 matches 1.. run data modify storage rpg:force p.c18 set value "#E6DFCF"
execute if score @s rpg_k18 matches 1.. run data modify storage rpg:force p.c18 set value "#A276BE"
scoreboard players add @s rpg_k19 0
execute store result storage rpg:force p.l19 int 1 run scoreboard players get @s rpg_k19
data modify storage rpg:force p.c19 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k18 matches 1.. run data modify storage rpg:force p.c19 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k18 matches 1.. run data modify storage rpg:force p.c19 set value "#E6DFCF"
execute if score @s rpg_k19 matches 1.. run data modify storage rpg:force p.c19 set value "#A276BE"
scoreboard players add @s rpg_k20 0
execute store result storage rpg:force p.l20 int 1 run scoreboard players get @s rpg_k20
data modify storage rpg:force p.c20 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k19 matches 1.. run data modify storage rpg:force p.c20 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k19 matches 1.. run data modify storage rpg:force p.c20 set value "#E6DFCF"
execute if score @s rpg_k20 matches 1.. run data modify storage rpg:force p.c20 set value "#A276BE"
scoreboard players add @s rpg_k21 0
execute store result storage rpg:force p.l21 int 1 run scoreboard players get @s rpg_k21
data modify storage rpg:force p.c21 set value "#5A5852"
execute if score @s rpg_force matches 2 run data modify storage rpg:force p.c21 set value "#E6DFCF"
execute if score @s rpg_force matches 3 run data modify storage rpg:force p.c21 set value "#E6DFCF"
execute if score @s rpg_k21 matches 1.. run data modify storage rpg:force p.c21 set value "#A276BE"
scoreboard players add @s rpg_k22 0
execute store result storage rpg:force p.l22 int 1 run scoreboard players get @s rpg_k22
data modify storage rpg:force p.c22 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k21 matches 1.. run data modify storage rpg:force p.c22 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k21 matches 1.. run data modify storage rpg:force p.c22 set value "#E6DFCF"
execute if score @s rpg_k22 matches 1.. run data modify storage rpg:force p.c22 set value "#A276BE"
scoreboard players add @s rpg_k23 0
execute store result storage rpg:force p.l23 int 1 run scoreboard players get @s rpg_k23
data modify storage rpg:force p.c23 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k22 matches 1.. run data modify storage rpg:force p.c23 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k22 matches 1.. run data modify storage rpg:force p.c23 set value "#E6DFCF"
execute if score @s rpg_k23 matches 1.. run data modify storage rpg:force p.c23 set value "#A276BE"
scoreboard players add @s rpg_k24 0
execute store result storage rpg:force p.l24 int 1 run scoreboard players get @s rpg_k24
data modify storage rpg:force p.c24 set value "#5A5852"
execute if score @s rpg_force matches 2 if score @s rpg_k23 matches 1.. run data modify storage rpg:force p.c24 set value "#E6DFCF"
execute if score @s rpg_force matches 3 if score @s rpg_k23 matches 1.. run data modify storage rpg:force p.c24 set value "#E6DFCF"
execute if score @s rpg_k24 matches 1.. run data modify storage rpg:force p.c24 set value "#A276BE"
function rpg:force/x/page/fill
data modify storage rpg:force p.h1 set value "—"
execute if score @s rpg_fs_h1 matches 25 run data modify storage rpg:force p.h1 set from storage rpg:force p.n25
execute if score @s rpg_fs_h1 matches 31 run data modify storage rpg:force p.h1 set from storage rpg:force p.n31
execute if score @s rpg_fs_h1 matches 32 run data modify storage rpg:force p.h1 set from storage rpg:force p.n32
execute if score @s rpg_fs_h1 matches 33 run data modify storage rpg:force p.h1 set from storage rpg:force p.n33
execute if score @s rpg_fs_h1 matches 34 run data modify storage rpg:force p.h1 set from storage rpg:force p.n34
execute if score @s rpg_fs_h1 matches 35 run data modify storage rpg:force p.h1 set from storage rpg:force p.n35
execute if score @s rpg_fs_h1 matches 36 run data modify storage rpg:force p.h1 set from storage rpg:force p.n36
execute if score @s rpg_fs_h1 matches 1 run data modify storage rpg:force p.h1 set value "圣光矛"
execute if score @s rpg_fs_h1 matches 2 run data modify storage rpg:force p.h1 set value "断罪印"
execute if score @s rpg_fs_h1 matches 3 run data modify storage rpg:force p.h1 set value "炽天之怒"
execute if score @s rpg_fs_h1 matches 4 run data modify storage rpg:force p.h1 set value "火焰之剑"
execute if score @s rpg_fs_h1 matches 5 run data modify storage rpg:force p.h1 set value "祝福"
execute if score @s rpg_fs_h1 matches 6 run data modify storage rpg:force p.h1 set value "庇护所"
execute if score @s rpg_fs_h1 matches 7 run data modify storage rpg:force p.h1 set value "洁净"
execute if score @s rpg_fs_h1 matches 8 run data modify storage rpg:force p.h1 set value "殉道"
execute if score @s rpg_fs_h1 matches 9 run data modify storage rpg:force p.h1 set value "显形"
execute if score @s rpg_fs_h1 matches 10 run data modify storage rpg:force p.h1 set value "圣链"
execute if score @s rpg_fs_h1 matches 11 run data modify storage rpg:force p.h1 set value "圣言"
execute if score @s rpg_fs_h1 matches 12 run data modify storage rpg:force p.h1 set value "升天"
data modify storage rpg:force p.h2 set value "—"
execute if score @s rpg_fs_h2 matches 25 run data modify storage rpg:force p.h2 set from storage rpg:force p.n25
execute if score @s rpg_fs_h2 matches 31 run data modify storage rpg:force p.h2 set from storage rpg:force p.n31
execute if score @s rpg_fs_h2 matches 32 run data modify storage rpg:force p.h2 set from storage rpg:force p.n32
execute if score @s rpg_fs_h2 matches 33 run data modify storage rpg:force p.h2 set from storage rpg:force p.n33
execute if score @s rpg_fs_h2 matches 34 run data modify storage rpg:force p.h2 set from storage rpg:force p.n34
execute if score @s rpg_fs_h2 matches 35 run data modify storage rpg:force p.h2 set from storage rpg:force p.n35
execute if score @s rpg_fs_h2 matches 36 run data modify storage rpg:force p.h2 set from storage rpg:force p.n36
execute if score @s rpg_fs_h2 matches 1 run data modify storage rpg:force p.h2 set value "圣光矛"
execute if score @s rpg_fs_h2 matches 2 run data modify storage rpg:force p.h2 set value "断罪印"
execute if score @s rpg_fs_h2 matches 3 run data modify storage rpg:force p.h2 set value "炽天之怒"
execute if score @s rpg_fs_h2 matches 4 run data modify storage rpg:force p.h2 set value "火焰之剑"
execute if score @s rpg_fs_h2 matches 5 run data modify storage rpg:force p.h2 set value "祝福"
execute if score @s rpg_fs_h2 matches 6 run data modify storage rpg:force p.h2 set value "庇护所"
execute if score @s rpg_fs_h2 matches 7 run data modify storage rpg:force p.h2 set value "洁净"
execute if score @s rpg_fs_h2 matches 8 run data modify storage rpg:force p.h2 set value "殉道"
execute if score @s rpg_fs_h2 matches 9 run data modify storage rpg:force p.h2 set value "显形"
execute if score @s rpg_fs_h2 matches 10 run data modify storage rpg:force p.h2 set value "圣链"
execute if score @s rpg_fs_h2 matches 11 run data modify storage rpg:force p.h2 set value "圣言"
execute if score @s rpg_fs_h2 matches 12 run data modify storage rpg:force p.h2 set value "升天"
data modify storage rpg:force p.h3 set value "—"
execute if score @s rpg_fs_h3 matches 25 run data modify storage rpg:force p.h3 set from storage rpg:force p.n25
execute if score @s rpg_fs_h3 matches 31 run data modify storage rpg:force p.h3 set from storage rpg:force p.n31
execute if score @s rpg_fs_h3 matches 32 run data modify storage rpg:force p.h3 set from storage rpg:force p.n32
execute if score @s rpg_fs_h3 matches 33 run data modify storage rpg:force p.h3 set from storage rpg:force p.n33
execute if score @s rpg_fs_h3 matches 34 run data modify storage rpg:force p.h3 set from storage rpg:force p.n34
execute if score @s rpg_fs_h3 matches 35 run data modify storage rpg:force p.h3 set from storage rpg:force p.n35
execute if score @s rpg_fs_h3 matches 36 run data modify storage rpg:force p.h3 set from storage rpg:force p.n36
execute if score @s rpg_fs_h3 matches 1 run data modify storage rpg:force p.h3 set value "圣光矛"
execute if score @s rpg_fs_h3 matches 2 run data modify storage rpg:force p.h3 set value "断罪印"
execute if score @s rpg_fs_h3 matches 3 run data modify storage rpg:force p.h3 set value "炽天之怒"
execute if score @s rpg_fs_h3 matches 4 run data modify storage rpg:force p.h3 set value "火焰之剑"
execute if score @s rpg_fs_h3 matches 5 run data modify storage rpg:force p.h3 set value "祝福"
execute if score @s rpg_fs_h3 matches 6 run data modify storage rpg:force p.h3 set value "庇护所"
execute if score @s rpg_fs_h3 matches 7 run data modify storage rpg:force p.h3 set value "洁净"
execute if score @s rpg_fs_h3 matches 8 run data modify storage rpg:force p.h3 set value "殉道"
execute if score @s rpg_fs_h3 matches 9 run data modify storage rpg:force p.h3 set value "显形"
execute if score @s rpg_fs_h3 matches 10 run data modify storage rpg:force p.h3 set value "圣链"
execute if score @s rpg_fs_h3 matches 11 run data modify storage rpg:force p.h3 set value "圣言"
execute if score @s rpg_fs_h3 matches 12 run data modify storage rpg:force p.h3 set value "升天"
data modify storage rpg:force p.m1 set value "—"
execute if score @s rpg_fs_m1 matches 26 run data modify storage rpg:force p.m1 set from storage rpg:force p.n26
execute if score @s rpg_fs_m1 matches 31 run data modify storage rpg:force p.m1 set from storage rpg:force p.n31
execute if score @s rpg_fs_m1 matches 32 run data modify storage rpg:force p.m1 set from storage rpg:force p.n32
execute if score @s rpg_fs_m1 matches 33 run data modify storage rpg:force p.m1 set from storage rpg:force p.n33
execute if score @s rpg_fs_m1 matches 34 run data modify storage rpg:force p.m1 set from storage rpg:force p.n34
execute if score @s rpg_fs_m1 matches 35 run data modify storage rpg:force p.m1 set from storage rpg:force p.n35
execute if score @s rpg_fs_m1 matches 36 run data modify storage rpg:force p.m1 set from storage rpg:force p.n36
execute if score @s rpg_fs_m1 matches 13 run data modify storage rpg:force p.m1 set value "暗焰"
execute if score @s rpg_fs_m1 matches 14 run data modify storage rpg:force p.m1 set value "血刃"
execute if score @s rpg_fs_m1 matches 15 run data modify storage rpg:force p.m1 set value "蚀骨"
execute if score @s rpg_fs_m1 matches 16 run data modify storage rpg:force p.m1 set value "深渊之口"
execute if score @s rpg_fs_m1 matches 17 run data modify storage rpg:force p.m1 set value "血肉护壳"
execute if score @s rpg_fs_m1 matches 18 run data modify storage rpg:force p.m1 set value "汲取"
execute if score @s rpg_fs_m1 matches 19 run data modify storage rpg:force p.m1 set value "献祭"
execute if score @s rpg_fs_m1 matches 21 run data modify storage rpg:force p.m1 set value "影步"
execute if score @s rpg_fs_m1 matches 22 run data modify storage rpg:force p.m1 set value "恐惧"
execute if score @s rpg_fs_m1 matches 23 run data modify storage rpg:force p.m1 set value "傀儡"
execute if score @s rpg_fs_m1 matches 24 run data modify storage rpg:force p.m1 set value "借柱"
data modify storage rpg:force p.m2 set value "—"
execute if score @s rpg_fs_m2 matches 26 run data modify storage rpg:force p.m2 set from storage rpg:force p.n26
execute if score @s rpg_fs_m2 matches 31 run data modify storage rpg:force p.m2 set from storage rpg:force p.n31
execute if score @s rpg_fs_m2 matches 32 run data modify storage rpg:force p.m2 set from storage rpg:force p.n32
execute if score @s rpg_fs_m2 matches 33 run data modify storage rpg:force p.m2 set from storage rpg:force p.n33
execute if score @s rpg_fs_m2 matches 34 run data modify storage rpg:force p.m2 set from storage rpg:force p.n34
execute if score @s rpg_fs_m2 matches 35 run data modify storage rpg:force p.m2 set from storage rpg:force p.n35
execute if score @s rpg_fs_m2 matches 36 run data modify storage rpg:force p.m2 set from storage rpg:force p.n36
execute if score @s rpg_fs_m2 matches 13 run data modify storage rpg:force p.m2 set value "暗焰"
execute if score @s rpg_fs_m2 matches 14 run data modify storage rpg:force p.m2 set value "血刃"
execute if score @s rpg_fs_m2 matches 15 run data modify storage rpg:force p.m2 set value "蚀骨"
execute if score @s rpg_fs_m2 matches 16 run data modify storage rpg:force p.m2 set value "深渊之口"
execute if score @s rpg_fs_m2 matches 17 run data modify storage rpg:force p.m2 set value "血肉护壳"
execute if score @s rpg_fs_m2 matches 18 run data modify storage rpg:force p.m2 set value "汲取"
execute if score @s rpg_fs_m2 matches 19 run data modify storage rpg:force p.m2 set value "献祭"
execute if score @s rpg_fs_m2 matches 21 run data modify storage rpg:force p.m2 set value "影步"
execute if score @s rpg_fs_m2 matches 22 run data modify storage rpg:force p.m2 set value "恐惧"
execute if score @s rpg_fs_m2 matches 23 run data modify storage rpg:force p.m2 set value "傀儡"
execute if score @s rpg_fs_m2 matches 24 run data modify storage rpg:force p.m2 set value "借柱"
data modify storage rpg:force p.m3 set value "—"
execute if score @s rpg_fs_m3 matches 26 run data modify storage rpg:force p.m3 set from storage rpg:force p.n26
execute if score @s rpg_fs_m3 matches 31 run data modify storage rpg:force p.m3 set from storage rpg:force p.n31
execute if score @s rpg_fs_m3 matches 32 run data modify storage rpg:force p.m3 set from storage rpg:force p.n32
execute if score @s rpg_fs_m3 matches 33 run data modify storage rpg:force p.m3 set from storage rpg:force p.n33
execute if score @s rpg_fs_m3 matches 34 run data modify storage rpg:force p.m3 set from storage rpg:force p.n34
execute if score @s rpg_fs_m3 matches 35 run data modify storage rpg:force p.m3 set from storage rpg:force p.n35
execute if score @s rpg_fs_m3 matches 36 run data modify storage rpg:force p.m3 set from storage rpg:force p.n36
execute if score @s rpg_fs_m3 matches 13 run data modify storage rpg:force p.m3 set value "暗焰"
execute if score @s rpg_fs_m3 matches 14 run data modify storage rpg:force p.m3 set value "血刃"
execute if score @s rpg_fs_m3 matches 15 run data modify storage rpg:force p.m3 set value "蚀骨"
execute if score @s rpg_fs_m3 matches 16 run data modify storage rpg:force p.m3 set value "深渊之口"
execute if score @s rpg_fs_m3 matches 17 run data modify storage rpg:force p.m3 set value "血肉护壳"
execute if score @s rpg_fs_m3 matches 18 run data modify storage rpg:force p.m3 set value "汲取"
execute if score @s rpg_fs_m3 matches 19 run data modify storage rpg:force p.m3 set value "献祭"
execute if score @s rpg_fs_m3 matches 21 run data modify storage rpg:force p.m3 set value "影步"
execute if score @s rpg_fs_m3 matches 22 run data modify storage rpg:force p.m3 set value "恐惧"
execute if score @s rpg_fs_m3 matches 23 run data modify storage rpg:force p.m3 set value "傀儡"
execute if score @s rpg_fs_m3 matches 24 run data modify storage rpg:force p.m3 set value "借柱"
