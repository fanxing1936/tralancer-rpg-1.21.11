# 一次性提示的渲染。按号分支 —— 与进度条走同一个出口，所以两者不会互相盖。
execute if entity @s[scores={rpg_hud_m=1}] run data modify storage rpg:hud e set value '["",{"text":"人偶碎了","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=1}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=2}] run data modify storage rpg:hud e set value '["",{"text":"星光照出了你身上的东西","italic":true,"color":"dark_red"}]'
execute if entity @s[scores={rpg_hud_m=2}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=3}] run data modify storage rpg:hud e set value '["",{"text":"[收割]","italic":false,"color":"#33C7B5","bold":true},{"text":"　灵魂离壳一寸","italic":false,"color":"#9ED8D0"},{"text":" ✦","italic":false,"color":"#E8FFFB"}]'
execute if entity @s[scores={rpg_hud_m=3}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=4}] run data modify storage rpg:hud e set value '["",{"text":"[余烬]","italic":false,"color":"#C66A45","bold":true},{"text":"　三重刀罡穿过灰幕","italic":false,"color":"#D8AAA0"},{"text":" ✦","italic":false,"color":"#FFF0E8"}]'
execute if entity @s[scores={rpg_hud_m=4}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=5}] run data modify storage rpg:hud e set value '["",{"text":"[朝拜]","italic":false,"color":"#9B6DE3","bold":true},{"text":"　暗之军团俯首","italic":false,"color":"#D3C0F0"},{"text":" ✦","italic":false,"color":"#F4ECFF"}]'
execute if entity @s[scores={rpg_hud_m=5}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=6}] run data modify storage rpg:hud e set value '["",{"text":"[血痂]","italic":false,"color":"#C63D52","bold":true},{"text":"　锯齿咬住了血肉","italic":false,"color":"#E2A5AF"},{"text":" ✦","italic":false,"color":"#FFE8EC"}]'
execute if entity @s[scores={rpg_hud_m=6}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=7}] run data modify storage rpg:hud e set value '["",{"text":"[怒嚎]","italic":false,"color":"#D99A35","bold":true},{"text":"　山脊在刃下开裂","italic":false,"color":"#E5C88D"},{"text":" ✦","italic":false,"color":"#FFF2D2"}]'
execute if entity @s[scores={rpg_hud_m=7}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=8}] run data modify storage rpg:hud e set value '["",{"text":"[漆黑之刃]","italic":false,"color":"#8359D6","bold":true},{"text":"　夜幕合拢","italic":false,"color":"#C4AFE8"},{"text":" ✦","italic":false,"color":"#F1E9FF"}]'
execute if entity @s[scores={rpg_hud_m=8}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=9}] run data modify storage rpg:hud e set value '["",{"text":"[着意·黑]","italic":false,"color":"#727680","bold":true},{"text":"　墨锋破敌","italic":false,"color":"#AEB2BA"},{"text":" ✦","italic":false,"color":"#E8E9EC"}]'
execute if entity @s[scores={rpg_hud_m=9}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=10}] run data modify storage rpg:hud e set value '["",{"text":"[着意·白]","italic":false,"color":"#F2F2F2","bold":true},{"text":"　留白回生","italic":false,"color":"#D6D9DE"},{"text":" ✦","italic":false,"color":"#FFFFFF"}]'
execute if entity @s[scores={rpg_hud_m=10}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=11}] run data modify storage rpg:hud e set value '["",{"text":"[王座]","italic":false,"color":"#FF3B1F","bold":true},{"text":"　受印者伏于枪下","italic":false,"color":"#FFB8A8"},{"text":" ✦","italic":false,"color":"#FFF0EC"}]'
execute if entity @s[scores={rpg_hud_m=11}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=12}] run data modify storage rpg:hud e set value '["",{"text":"[狂风]","italic":false,"color":"#63B94B","bold":true},{"text":"　三道风路并起","italic":false,"color":"#BEE5B2"},{"text":" ✦","italic":false,"color":"#F0FFE9"}]'
execute if entity @s[scores={rpg_hud_m=12}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=13}] run data modify storage rpg:hud e set value '["",{"text":"[淬毒]","italic":false,"color":"#5FAF2D","bold":true},{"text":"　三痕归一，蛇毒入骨","italic":false,"color":"#B7E37E"},{"text":" ✦","italic":false,"color":"#EEFFD5"}]'
execute if entity @s[scores={rpg_hud_m=13}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=14}] run data modify storage rpg:hud e set value '["",{"text":"[严寒风暴]","italic":false,"color":"#45C9E8","bold":true},{"text":"　冻原扩张","italic":false,"color":"#BDEFFF"},{"text":" ✦","italic":false,"color":"#F2FDFF"}]'
execute if entity @s[scores={rpg_hud_m=14}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=15}] run data modify storage rpg:hud e set value '["",{"text":"[珊瑚突刺]","italic":false,"color":"#E56DB8","bold":true},{"text":"　潮锋贯出","italic":false,"color":"#FFC4E6"},{"text":" ✦","italic":false,"color":"#FFF0F9"}]'
execute if entity @s[scores={rpg_hud_m=15}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=16}] run data modify storage rpg:hud e set value '["",{"text":"[漆黑]","italic":false,"color":"#8155D9","bold":true},{"text":"　夜幕合拢","italic":false,"color":"#C5B1EB"},{"text":" ✦","italic":false,"color":"#F1EAFF"}]'
execute if entity @s[scores={rpg_hud_m=16}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=17}] run data modify storage rpg:hud e set value '["",{"text":"[樱怒]","italic":false,"color":"#FF6F91","bold":true},{"text":"　四景尽斩","italic":false,"color":"#FFD1DC"},{"text":" ✦","italic":false,"color":"#FFF0F5"}]'
execute if entity @s[scores={rpg_hud_m=17}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=18}] run data modify storage rpg:hud e set value '["",{"text":"法力枯竭","italic":true,"color":"gray"},{"text":" · 需要 1 级经验","italic":false,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_m=18}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=19}] run data modify storage rpg:hud e set value '["",{"text":"[烈焰]","italic":false,"color":"#FF5A36","bold":true},{"text":"　焚尽前路","italic":false,"color":"#FFC0AA"},{"text":" ✦","italic":false,"color":"#FFF0E8"}]'
execute if entity @s[scores={rpg_hud_m=19}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=20}] run data modify storage rpg:hud e set value '["",{"text":"[钢刃]","italic":false,"color":"#55C6E3","bold":true},{"text":"　剑气出鞘","italic":false,"color":"#BFEAF4"},{"text":" ✦","italic":false,"color":"#F3FDFF"}]'
execute if entity @s[scores={rpg_hud_m=20}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=21}] run data modify storage rpg:hud e set value '["",{"text":"[风暴]","italic":false,"color":"#59B94C","bold":true},{"text":"　风弹离手","italic":false,"color":"#BFE4B5"},{"text":" ✦","italic":false,"color":"#F0FFE9"}]'
execute if entity @s[scores={rpg_hud_m=21}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=22}] run data modify storage rpg:hud e set value '["",{"text":"[买断]","italic":false,"color":"#B7950B","bold":true},{"text":"　金箭离弦","italic":false,"color":"#FFD700"},{"text":" ✦","italic":false,"color":"#FFF2A8"}]'
execute if entity @s[scores={rpg_hud_m=22}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=23}] run data modify storage rpg:hud e set value '["",{"text":"[买断]","italic":false,"color":"#B7950B","bold":true},{"text":"　付不起 —— 于是拿命抵了","italic":false,"color":"dark_red"}]'
execute if entity @s[scores={rpg_hud_m=23}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=24}] run data modify storage rpg:hud e set value '["",{"text":"[买断]","italic":false,"color":"#B7950B","bold":true},{"text":"　付讫：5 级","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=24}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=25}] run data modify storage rpg:hud e set value '["",{"text":"[通行费]","italic":false,"color":"#B7950B","bold":true},{"text":"　玛门收走了 6 点经验","italic":false,"color":"#B7950B","bold":false}]'
execute if entity @s[scores={rpg_hud_m=25}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=26}] run data modify storage rpg:hud e set value '["",{"text":"[什一税]","italic":false,"color":"#B7950B","bold":true},{"text":"　玛门收走了 1 枚","italic":false,"color":"#B7950B","bold":false}]'
execute if entity @s[scores={rpg_hud_m=26}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=27}] run data modify storage rpg:hud e set value '["",{"text":"[血税]","italic":false,"color":"#B7950B","bold":true},{"text":"　玛门称走了你的一份血","italic":false,"color":"#B7950B","bold":false}]'
execute if entity @s[scores={rpg_hud_m=27}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=28}] run data modify storage rpg:hud e set value '["",{"text":"[饥荒]","italic":false,"color":"#B7950B","bold":true},{"text":"　你的下一顿也被算进账里","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=28}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=29}] run data modify storage rpg:hud e set value '["",{"text":"[贪得无厌]","italic":false,"color":"#B7950B","bold":true},{"text":"　这一箭，玛门收了两样","italic":false,"color":"dark_red"}]'
execute if entity @s[scores={rpg_hud_m=29}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=30}] run data modify storage rpg:hud e set value '["",{"text":"[什一税]","italic":false,"color":"#B7950B","bold":true},{"text":"　柱中的东西替你付了账","italic":false,"color":"dark_red"}]'
execute if entity @s[scores={rpg_hud_m=30}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=31}] run data modify storage rpg:hud e set value '["",{"text":"你已与另一柱立约","italic":true,"color":"dark_red"}]'
execute if entity @s[scores={rpg_hud_m=31}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=32}] run data modify storage rpg:hud e set value '["",{"text":"图腾已尽","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=32}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=33}] run data modify storage rpg:hud e set value '["",{"text":"驱　魔","color":"gold","bold":true},{"text":"　图腾开始燃尽","color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=33}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=34}] run data modify storage rpg:hud e set value '["",{"text":"图腾已立","color":"gold"},{"text":"　以驱魔圣水浇之","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=34}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=35}] run data modify storage rpg:hud e set value '["",{"text":"已解雇","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=35}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=36}] run data modify storage rpg:hud e set value '["",{"text":"小队已满员","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=36}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=37}] run data modify storage rpg:hud e set value '["",{"text":"已配装","color":"#D4AF37"}]'
execute if entity @s[scores={rpg_hud_m=37}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=38}] run data modify storage rpg:hud e set value '["",{"text":"视线里没有目标","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=38}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=39}] run data modify storage rpg:hud e set value '["",{"text":"你还没有小队","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=39}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=40}] run data modify storage rpg:hud e set value '["",{"text":"身边没有自己的佣兵","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=40}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=41}] run data modify storage rpg:hud e set value '["",{"text":"钱不够","italic":true,"color":"red"}]'
execute if entity @s[scores={rpg_hud_m=41}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=42}] run data modify storage rpg:hud e set value '["",{"text":"待雇 · HAIKU","color":"gray","bold":true},{"text":"　8 枚　再次长按雇下他","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=42}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=43}] run data modify storage rpg:hud e set value '["",{"text":"待雇 · SONNET","color":"#57C6D6","bold":true},{"text":"　20 枚　再次长按雇下他","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=43}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=44}] run data modify storage rpg:hud e set value '["",{"text":"待雇 · OPUS","color":"#A275DE","bold":true},{"text":"　40 枚　再次长按雇下他","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=44}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=45}] run data modify storage rpg:hud e set value '["",{"text":"待雇 · FABLE","color":"#D9A02B","bold":true},{"text":"　80 枚　再次长按雇下他","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=45}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=46}] run data modify storage rpg:hud e set value '["",{"text":"待雇 · MYTHOS","color":"#FFD700","bold":true},{"text":"　160 枚　再次长按雇下他","color":"gray","italic":true}]'
execute if entity @s[scores={rpg_hud_m=46}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=47}] run data modify storage rpg:hud e set value '["",{"text":"跟　随","color":"#D4AF37","bold":true}]'
execute if entity @s[scores={rpg_hud_m=47}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=48}] run data modify storage rpg:hud e set value '["",{"text":"驻　守","color":"#8FA1B3","bold":true}]'
execute if entity @s[scores={rpg_hud_m=48}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=49}] run data modify storage rpg:hud e set value '["",{"text":"佣兵已入队","color":"#D4AF37"}]'
execute if entity @s[scores={rpg_hud_m=49}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=50}] run data modify storage rpg:hud e set value '["",{"text":"已晋升 · SONNET","italic":false,"color":"#57C6D6","bold":true}]'
execute if entity @s[scores={rpg_hud_m=50}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=51}] run data modify storage rpg:hud e set value '["",{"text":"已晋升 · OPUS","italic":false,"color":"#A275DE","bold":true}]'
execute if entity @s[scores={rpg_hud_m=51}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=52}] run data modify storage rpg:hud e set value '["",{"text":"已晋升 · FABLE","italic":false,"color":"#D9A02B","bold":true}]'
execute if entity @s[scores={rpg_hud_m=52}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=53}] run data modify storage rpg:hud e set value '["",{"text":"已晋升 · MYTHOS","italic":false,"color":"#FFD700","bold":true}]'
execute if entity @s[scores={rpg_hud_m=53}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=54}] run data modify storage rpg:hud e set value '["",{"text":"他已经是 MYTHOS 了","italic":true,"color":"#D4AF37"}]'
execute if entity @s[scores={rpg_hud_m=54}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=55}] run data modify storage rpg:hud e set value '["",{"text":"人偶替你受下了","italic":true,"color":"#C9A227"}]'
execute if entity @s[scores={rpg_hud_m=55}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=56}] run data modify storage rpg:hud e set value '["",{"text":"圣痕淡去","italic":true,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_m=56}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=57}] run data modify storage rpg:hud e set value '["",{"text":"你打碎的只是空壳","italic":true,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_m=57}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=58}] run data modify storage rpg:hud e set value '["",{"text":"壳裂开了","italic":true,"color":"dark_purple"}]'
execute if entity @s[scores={rpg_hud_m=58}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=59}] run data modify storage rpg:hud e set value '["",{"text":"[十诫净界]","color":"#D4AF37","bold":true,"italic":false},{"text":"　律法涤尽十方罪影","color":"#FFF2A8","bold":false,"italic":false},{"text":" ✦","color":"#FFFFFF","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=59}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=60}] run data modify storage rpg:hud e set value '["",{"text":"[创世净光]","color":"#62D9E8","bold":true,"italic":false},{"text":"　权柄化作前路之光","color":"#E8F4FF","bold":false,"italic":false},{"text":" ✦","color":"#FFFFFF","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=60}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=61}] run data modify storage rpg:hud e set value '["",{"text":"[伊甸敕界]","color":"#FFF2A8","bold":true,"italic":false},{"text":"　伊甸在脚下重开","color":"#E8F4FF","bold":false,"italic":false},{"text":" ✦","color":"#FFFFFF","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=61}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=62}] run data modify storage rpg:hud e set value '["",{"text":"[赦免]","color":"#62D9E8","bold":true,"italic":false},{"text":"　柱中之力未留下魔化","color":"gray","bold":false,"italic":false},{"text":" ✦","color":"#FFF2A8","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=62}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=63}] run data modify storage rpg:hud e set value '["",{"text":"[终末圣裁]","color":"#62D9E8","bold":true,"italic":false},{"text":"　权柄已覆于下一击","color":"#E8F4FF","bold":false,"italic":false},{"text":" ✦","color":"#FFF2A8","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=63}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=64}] run data modify storage rpg:hud e set value '["",{"text":"[圣子恩赐]","color":"#FFF2A8","bold":true,"italic":false},{"text":"　生命在他者身上续行","color":"#E8F4FF","bold":false,"italic":false},{"text":" ✦","color":"#FFFFFF","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=64}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_m=65}] run data modify storage rpg:hud e set value '["",{"text":"[终末圣裁]","color":"#62D9E8","bold":true,"italic":false},{"text":"　罪秽在审判中消散","color":"#FFF2A8","bold":false,"italic":false},{"text":" ✦","color":"#FFFFFF","bold":false,"italic":false}]'
execute if entity @s[scores={rpg_hud_m=65}] run function rpg:hud/seal/event with storage rpg:hud
