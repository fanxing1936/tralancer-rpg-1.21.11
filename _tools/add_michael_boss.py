# -*- coding: utf-8 -*-
"""天使长米迦勒 Boss（docs/MICHAEL-DESIGN.md）。只用指令召唤，规格对齐教皇战、篡夺者、雅克、扫罗。

    python add_michael_boss.py ../rpg

外观在 add_michael_model.py（载体 rpg.mkb 换装为 rpg.mkm；守望者 rpg.mkw 换装为 rpg.mkwm），
血条、羽毛与骨头的物品模型在 add_michael_boss_art.py；特效贴图是米迦勒专属的（add_michael_fx_art.py：原作素材加 Codex 序列帧，
颜色烘焙在贴图里），由 michael_boss_lib.MichaelFx 接到 boss_fx 上。
代码分四个文件：michael_boss_lib（常量与小工具）、_frame（框架）、_skills（招式、守望者、注视、圣焰）、_ults（大招与特效）。

两段，每段 1200 血：一阶段「天使长·谁似神」持脊骨；骨中之骨（脊骨插进场地中心成骨柱）；二阶段「炽天使」持双肋骨。
每段一池血，切段补满；副手放隐形的死亡保护，致命一击被它吃掉后由切段接手（同扫罗）。
他是天使：载体不带 rpg.demon（七罪契约打不到），也不带 rpg.demon.fly（新约打不到）。

伤害怎么算（玩家打到他时当场判定，下一刻按伤害统计的增量结算，同扫罗的 hit/settle）：
  显形中（破绽）          → 这一下再多扣一半；
  六翼掩面中              → 退回八成；
  还有守望者活着（被看见） → 退回三成。
"""
import os

from michael_boss_lib import B, DP, OUT, fx, hook_tag, w, MAX
import michael_boss_frame as frame
import michael_boss_skills as skills
import michael_boss_ults as ults

FX_TICK = ("walker", "feather", "trail", "rainf", "rainfeather", "spoke", "wave", "orb", "trump", "meteor", "bigstar")


def main():
    frame.build()
    skills.skills1()
    skills.skills2()
    ults.ults1()
    ults.ults2()
    ults.vfx()
    fx.build(extra_tick=["execute if entity @s[tag=rpg.mkb.%s] run return run function %s/fx/%s" % (k, B, k) for k in FX_TICK])
    # 序章模式的血线钩子：默认空标签，add_prologue.py 往里登记自己的函数（没有序章时这一行什么也不做）
    tag = os.path.join(DP, "data", "rpg", "tags", "function", "michael_boss", "prologue_hp.json")
    os.makedirs(os.path.dirname(tag), exist_ok=True)
    with open(tag, "w", encoding="utf-8") as fh:
        fh.write('{"values": []}' + chr(10))
    hook_tag(DP, "load", "%s/load" % B, False)
    hook_tag(DP, "tick", "%s/tick" % B, True)
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("michael_boss: %d functions; two stages of %d HP" % (count, MAX))


if __name__ == "__main__":
    main()
