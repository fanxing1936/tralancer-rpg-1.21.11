# 选中：记下坐标，把整座镇的范围 forceload 上，等区块到齐再建
function rpg:town/job/fl_rem with storage rpg:town m
scoreboard players operation #h0 rpg_tw = #mn rpg_tw
scoreboard players operation #h0 rpg_tw += #mx rpg_tw
scoreboard players operation #h0 rpg_tw /= #2 rpg_tw
execute if score #cur rpg_tw matches 1 run scoreboard players operation #x1 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 1 run scoreboard players operation #z1 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 1 run scoreboard players operation #v1 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 1 run scoreboard players set #r rpg_tw 153
execute if score #cur rpg_tw matches 2 run scoreboard players operation #x2 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 2 run scoreboard players operation #z2 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 2 run scoreboard players operation #v2 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 2 run scoreboard players set #r rpg_tw 171
execute if score #cur rpg_tw matches 3 run scoreboard players operation #x3 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 3 run scoreboard players operation #z3 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 3 run scoreboard players operation #v3 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 3 run scoreboard players set #r rpg_tw 159
execute if score #cur rpg_tw matches 4 run scoreboard players operation #x4 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 4 run scoreboard players operation #z4 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 4 run scoreboard players operation #v4 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 4 run scoreboard players set #r rpg_tw 150
execute if score #cur rpg_tw matches 5 run scoreboard players operation #x5 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 5 run scoreboard players operation #z5 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 5 run scoreboard players operation #v5 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 5 run scoreboard players set #r rpg_tw 174
execute if score #cur rpg_tw matches 6 run scoreboard players operation #x6 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 6 run scoreboard players operation #z6 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 6 run scoreboard players operation #v6 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 6 run scoreboard players set #r rpg_tw 147
execute if score #cur rpg_tw matches 7 run scoreboard players operation #x7 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 7 run scoreboard players operation #z7 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 7 run scoreboard players operation #v7 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 7 run scoreboard players set #r rpg_tw 155
execute if score #cur rpg_tw matches 8 run scoreboard players operation #x8 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 8 run scoreboard players operation #z8 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 8 run scoreboard players operation #v8 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 8 run scoreboard players set #r rpg_tw 174
execute if score #cur rpg_tw matches 9 run scoreboard players operation #x9 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 9 run scoreboard players operation #z9 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 9 run scoreboard players operation #v9 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 9 run scoreboard players set #r rpg_tw 153
execute if score #cur rpg_tw matches 10 run scoreboard players operation #x10 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 10 run scoreboard players operation #z10 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 10 run scoreboard players operation #v10 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 10 run scoreboard players set #r rpg_tw 174
execute if score #cur rpg_tw matches 11 run scoreboard players operation #x11 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 11 run scoreboard players operation #z11 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 11 run scoreboard players operation #v11 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 11 run scoreboard players set #r rpg_tw 171
execute if score #cur rpg_tw matches 12 run scoreboard players operation #x12 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 12 run scoreboard players operation #z12 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 12 run scoreboard players operation #v12 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 12 run scoreboard players set #r rpg_tw 167
execute if score #cur rpg_tw matches 13 run scoreboard players operation #x13 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 13 run scoreboard players operation #z13 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 13 run scoreboard players operation #v13 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 13 run scoreboard players set #r rpg_tw 156
execute if score #cur rpg_tw matches 14 run scoreboard players operation #x14 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 14 run scoreboard players operation #z14 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 14 run scoreboard players operation #v14 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 14 run scoreboard players set #r rpg_tw 160
execute if score #cur rpg_tw matches 15 run scoreboard players operation #x15 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 15 run scoreboard players operation #z15 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 15 run scoreboard players operation #v15 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 15 run scoreboard players set #r rpg_tw 152
execute if score #cur rpg_tw matches 16 run scoreboard players operation #x16 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 16 run scoreboard players operation #z16 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 16 run scoreboard players operation #v16 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 16 run scoreboard players set #r rpg_tw 174
execute if score #cur rpg_tw matches 17 run scoreboard players operation #x17 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 17 run scoreboard players operation #z17 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 17 run scoreboard players operation #v17 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 17 run scoreboard players set #r rpg_tw 150
execute if score #cur rpg_tw matches 18 run scoreboard players operation #x18 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 18 run scoreboard players operation #z18 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 18 run scoreboard players operation #v18 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 18 run scoreboard players set #r rpg_tw 159
execute if score #cur rpg_tw matches 19 run scoreboard players operation #x19 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 19 run scoreboard players operation #z19 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 19 run scoreboard players operation #v19 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 19 run scoreboard players set #r rpg_tw 166
execute if score #cur rpg_tw matches 20 run scoreboard players operation #x20 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 20 run scoreboard players operation #z20 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 20 run scoreboard players operation #v20 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 20 run scoreboard players set #r rpg_tw 151
execute if score #cur rpg_tw matches 21 run scoreboard players operation #x21 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 21 run scoreboard players operation #z21 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 21 run scoreboard players operation #v21 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 21 run scoreboard players set #r rpg_tw 138
execute if score #cur rpg_tw matches 22 run scoreboard players operation #x22 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 22 run scoreboard players operation #z22 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 22 run scoreboard players operation #v22 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 22 run scoreboard players set #r rpg_tw 138
execute if score #cur rpg_tw matches 23 run scoreboard players operation #x23 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 23 run scoreboard players operation #z23 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 23 run scoreboard players operation #v23 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 23 run scoreboard players set #r rpg_tw 138
execute if score #cur rpg_tw matches 24 run scoreboard players operation #x24 rpg_tw = #px rpg_tw
execute if score #cur rpg_tw matches 24 run scoreboard players operation #z24 rpg_tw = #pz rpg_tw
execute if score #cur rpg_tw matches 24 run scoreboard players operation #v24 rpg_tw = #v rpg_tw
execute if score #cur rpg_tw matches 24 run scoreboard players set #r rpg_tw 138
function rpg:town/job/bigcoords
function rpg:town/job/big_add with storage rpg:town m
scoreboard players set #wt rpg_tw 0
scoreboard players set #ph rpg_tw 2
execute if score #cur rpg_tw matches 1 run scoreboard players set #s1 rpg_tw 2
execute if score #cur rpg_tw matches 2 run scoreboard players set #s2 rpg_tw 2
execute if score #cur rpg_tw matches 3 run scoreboard players set #s3 rpg_tw 2
execute if score #cur rpg_tw matches 4 run scoreboard players set #s4 rpg_tw 2
execute if score #cur rpg_tw matches 5 run scoreboard players set #s5 rpg_tw 2
execute if score #cur rpg_tw matches 6 run scoreboard players set #s6 rpg_tw 2
execute if score #cur rpg_tw matches 7 run scoreboard players set #s7 rpg_tw 2
execute if score #cur rpg_tw matches 8 run scoreboard players set #s8 rpg_tw 2
execute if score #cur rpg_tw matches 9 run scoreboard players set #s9 rpg_tw 2
execute if score #cur rpg_tw matches 10 run scoreboard players set #s10 rpg_tw 2
execute if score #cur rpg_tw matches 11 run scoreboard players set #s11 rpg_tw 2
execute if score #cur rpg_tw matches 12 run scoreboard players set #s12 rpg_tw 2
execute if score #cur rpg_tw matches 13 run scoreboard players set #s13 rpg_tw 2
execute if score #cur rpg_tw matches 14 run scoreboard players set #s14 rpg_tw 2
execute if score #cur rpg_tw matches 15 run scoreboard players set #s15 rpg_tw 2
execute if score #cur rpg_tw matches 16 run scoreboard players set #s16 rpg_tw 2
execute if score #cur rpg_tw matches 17 run scoreboard players set #s17 rpg_tw 2
execute if score #cur rpg_tw matches 18 run scoreboard players set #s18 rpg_tw 2
execute if score #cur rpg_tw matches 19 run scoreboard players set #s19 rpg_tw 2
execute if score #cur rpg_tw matches 20 run scoreboard players set #s20 rpg_tw 2
execute if score #cur rpg_tw matches 21 run scoreboard players set #s21 rpg_tw 2
execute if score #cur rpg_tw matches 22 run scoreboard players set #s22 rpg_tw 2
execute if score #cur rpg_tw matches 23 run scoreboard players set #s23 rpg_tw 2
execute if score #cur rpg_tw matches 24 run scoreboard players set #s24 rpg_tw 2
