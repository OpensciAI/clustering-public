%% Determine which symptom frequencies vary by menopausal status
group1=length(premenopausalsymptomscorrect.bloating)
group2=length(menopausalsymptomstest1.bloating)
groupidx=vertcat(zeros(group1,1),ones(group2,1));
[pbloating,tblbloating,statsbloating]=kruskalwallis([premenopausalsymptomscorrect.bloating; menopausalsymptomstest1.bloating],groupidx);
%c=multcompare(statsdbt,'Alpha',0.05); 


% Create a list of symptom names
% Get the variable names (header names) of the table
symptomNames = premenopausalsymptomscorrect.Properties.VariableNames; % Add all the symptom names here

% Initialize result arrays to store the p-value, table, and stats for each symptom
numSymptoms = length(symptomNames);
pValues = zeros(numSymptoms, 1);
resultTables = cell(numSymptoms, 1);
statistics = cell(numSymptoms, 1);

% Loop through each symptom and perform the Kruskal-Wallis test
for i = 2:numSymptoms
    symptomName = symptomNames{i};
    
    % Get the data for the current symptom from the respective tables
    dataGroup1 = premenopausalsymptomscorrect.(symptomName);
    dataGroup2 = menopausalsymptomstest1.(symptomName);
    
    % Create the group index for the Kruskal-Wallis test
    group1 = length(dataGroup1);
    group2 = length(dataGroup2);
    groupidx = vertcat(zeros(group1, 1), ones(group2, 1));
    
    % Perform the Kruskal-Wallis test for the current symptom
    [p, tbl, stats] = kruskalwallis([dataGroup1; dataGroup2], groupidx);
    
    % Store the results for the current symptom
    pValues(i) = p;
    Chisq(i)=tbl{2,5};
    resultTables{i} = tbl;
    statistics{i} = stats;
end

% Create a table with symptom names as headers and data from the respective arrays
resultsTable = table(symptomNames.', pValues,Chisq', resultTables, statistics, ...
                     'VariableNames', {'Symptom', 'P_Value', 'Chi-sq','Result_Table', 'Statistics'});




%most symptoms exhibited a statistical difference in symptom burden. Aside
%from hot flashes, and night sweats (which were not present in
%premenopausal users); and ovulation and ovulation pain,(which were not
%present in menopausal users), the largest group differences were in
% 
% - cramps (pre)
% - breast pain (pre)
% - fatigue (pre)
% - bloating (pre)
% - headaches (pre)
% - breast swelling (pre)
% - diarrhea (almost identical)
% - anxiety (pre by a lot!)
% - mood swings (identical)
% - painful sex

% 
% %No differences were observed in
% 'uti'	0.0508270419954021	3.81396354413112
% 'nipple_discharge'	0.0873289158526334	2.92293450079367
% 'facial_hair'	0.101771805008739	2.67755608795936
% 'hair_loss'	0.109686206444361	2.55873661876632
% 'tingling_extremeties'	0.299786166064668	1.07514513815826
% 'incontinence'	0.452248028857371	0.565011555153443
% 'vomiting'	0.491352119472976	0.473563990108551
% 'chills'	0.524504895270224	0.405026144988019
% 'heartburn'	0.612201095681479	0.256982127723918
% 'yeast_infection'	0.746465496759566	0.104525073565775