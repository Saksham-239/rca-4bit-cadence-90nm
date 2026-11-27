%% Reproducible performance plots for the four-bit RCA case study
% Requires MATLAB R2025b or a recent release with exportgraphics/tiledlayout.

scriptDir = fileparts(mfilename('fullpath'));
repoRoot = fileparts(fileparts(scriptDir));
outputDir = fullfile(repoRoot, 'assets', 'plots');
if ~isfolder(outputDir)
    mkdir(outputDir);
end

logicFamilies = {'Static CMOS', 'C^{2}MOS', 'Domino Logic'};
delayPs = [251.81, 260.75, 222.35];
averagePowerUw = [13.25, 29.49, 30.76];
pdpFj = averagePowerUw .* delayPs ./ 1000;

expectedPdpFj = [3.34, 7.69, 6.84];
assert(isequal(round(pdpFj, 2), expectedPdpFj), ...
    'Recalculated PDP values do not match the expected rounded values.');

% Dark blue, orange and gray retain distinct luminance in grayscale output.
barColors = [0.12, 0.34, 0.52; ...
             0.82, 0.40, 0.12; ...
             0.42, 0.42, 0.42];

makeBarFigure(logicFamilies, pdpFj, barColors, ...
    'Power-Delay Product Comparison', 'Power-Delay Product (fJ)', ...
    'Lower PDP is better', '%.2f fJ', outputDir, 'pdp_comparison', [0, 8.8]);

makeBarFigure(logicFamilies, delayPs, barColors, ...
    'Propagation Delay Comparison', 'Propagation Delay (ps)', ...
    'Domino is fastest in this dataset', '%.2f ps', ...
    outputDir, 'delay_comparison', [0, 300]);

makeBarFigure(logicFamilies, averagePowerUw, barColors, ...
    'Average Power Comparison', 'Average Power (\muW)', ...
    'Static CMOS has the lowest reported average power', '%.2f µW', ...
    outputDir, 'power_comparison', [0, 36]);

% Optional overview: each panel has its own zero-based axis and units.
overview = figure('Color', 'white', 'Units', 'inches', ...
    'Position', [1, 1, 12.4, 4.4], 'Renderer', 'painters');
layout = tiledlayout(overview, 1, 3, 'TileSpacing', 'compact', ...
    'Padding', 'compact');
overviewLabels = {'Static', 'C^{2}MOS', 'Domino'};
ax = nexttile(layout);
paintBars(ax, overviewLabels, pdpFj, barColors, ...
    'PDP (fJ)', '%.2f');
ax.FontSize = 8;
ylim(ax, [0, 9.2]);
title(ax, 'PDP', 'FontWeight', 'bold', 'Color', [0.10, 0.10, 0.10]);
ax = nexttile(layout);
paintBars(ax, overviewLabels, delayPs, barColors, ...
    'Delay (ps)', '%.1f');
ax.FontSize = 8;
title(ax, 'Propagation Delay', 'FontWeight', 'bold', 'Color', [0.10, 0.10, 0.10]);
ax = nexttile(layout);
paintBars(ax, overviewLabels, averagePowerUw, barColors, ...
    'Average Power (\muW)', '%.1f');
ax.FontSize = 8;
title(ax, 'Average Power', 'FontWeight', 'bold', 'Color', [0.10, 0.10, 0.10]);
sgtitle(layout, 'Four-Bit RCA Performance Overview', ...
    'FontWeight', 'bold', 'FontSize', 13, 'Color', [0.10, 0.10, 0.10]);
exportPlot(overview, outputDir, 'combined_performance');
close(overview);

fprintf('Recalculated PDP (fJ): Static CMOS %.6f, C^2MOS %.6f, Domino %.6f\n', ...
    pdpFj(1), pdpFj(2), pdpFj(3));
fprintf('Rounded PDP (fJ): %.2f, %.2f, %.2f\n', ...
    round(pdpFj(1), 2), round(pdpFj(2), 2), round(pdpFj(3), 2));
fprintf('Plots saved under: %s\n', outputDir);

function makeBarFigure(labels, values, colors, plotTitle, yLabel, note, ...
    valueFormat, outputDir, fileStem, yLimits)
fig = figure('Color', 'white', 'Units', 'inches', ...
    'Position', [1, 1, 7.4, 4.8], 'Renderer', 'painters');
ax = axes(fig);
paintBars(ax, labels, values, colors, yLabel, valueFormat);
t = title(ax, plotTitle, 'FontWeight', 'bold', 'FontSize', 14);
t.Color = [0.10, 0.10, 0.10];
st = subtitle(ax, note, 'FontSize', 10);
st.Color = [0.20, 0.20, 0.20];
ylim(ax, yLimits);
exportPlot(fig, outputDir, fileStem);
close(fig);
end

function paintBars(ax, labels, values, colors, yLabel, valueFormat)
barHandle = bar(ax, values, 'BarWidth', 0.62, 'FaceColor', 'flat', ...
    'EdgeColor', [0.12, 0.12, 0.12], 'LineWidth', 0.7);
barHandle.CData = colors;
ax.Color = 'white';
ax.FontName = 'Arial';
ax.FontSize = 10;
ax.XColor = [0.12, 0.12, 0.12];
ax.YColor = [0.12, 0.12, 0.12];
ax.LineWidth = 0.8;
ax.Box = 'off';
ax.TickDir = 'out';
ax.Toolbar.Visible = 'off';
ax.XTick = 1:numel(labels);
ax.XTickLabel = labels;
ax.YLim(1) = 0;
ax.YGrid = 'on';
ax.XGrid = 'off';
ax.GridColor = [0.25, 0.25, 0.25];
ax.GridAlpha = 0.16;
ax.MinorGridAlpha = 0.08;
ylabel(ax, yLabel, 'FontName', 'Arial', 'FontSize', 11);
hold(ax, 'on');
labelOffset = 0.025 * max(values);
for k = 1:numel(values)
    text(ax, k, values(k) + labelOffset, sprintf(valueFormat, values(k)), ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
        'FontName', 'Arial', 'FontSize', 10, 'Color', [0.12, 0.12, 0.12]);
end
hold(ax, 'off');
end

function exportPlot(fig, outputDir, fileStem)
exportgraphics(fig, fullfile(outputDir, [fileStem, '.pdf']), ...
    'ContentType', 'vector', 'BackgroundColor', 'white');
exportgraphics(fig, fullfile(outputDir, [fileStem, '.png']), ...
    'Resolution', 300, 'BackgroundColor', 'white');
end
