(function () {
    let originalCompile;
    let wrappedCompile;
    const projectNames = new Set([
        'mossy_skeleton_body_original',
        'root_rot_armor_original',
        'lucifer_original_assembly',
        'verdant_robe_original',
        'lucifer',
        'lucifer_verdant',
        'lucifer_cuboid_wings',
        'lucifer_cuboid_wings_candidate'
    ]);
    Plugin.register('lucifer_source_precision', {
        title: 'Lucifer Original Asset Precision',
        author: 'Codex',
        description: 'Preserves source floating-point values when saving the two original Lucifer asset projects.',
        icon: 'precision_manufacturing',
        version: '1.0.1',
        min_version: '5.2.0',
        variant: 'desktop',
        onload() {
            originalCompile = Codecs.project.compile;
            wrappedCompile = function (options) {
                if (!projectNames.has(Project.name) || options?.raw || options?.compressed) {
                    return originalCompile.call(this, options);
                }
                const raw = originalCompile.call(this, Object.assign({}, options, {raw: true}));
                raw.meta.source_precision = 'native codec data; unrounded JSON numbers';
                return JSON.stringify(raw, null, options?.minify ? 0 : 2) + '\n';
            };
            Codecs.project.compile = wrappedCompile;
        },
        onunload() {
            if (Codecs.project.compile === wrappedCompile) Codecs.project.compile = originalCompile;
        }
    });
})();
