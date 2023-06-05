%%         What are p-values? - a computational approach 
% ------------------------------------------------------------------
% Restating arguments from https://f1000research.com/articles/4-621/v3
% ------------------------------------------------------------------

%% Definition
% a p-value is the probability of observing a result at least as extreme 
% as a test statistic (e.g. t value), assuming the null hypothesis of no 
% effect is true. 

% consider two variables X and Y, and the t statistic associated to their
% difference

X = randn(100,1) + 0.25; % expected mean 0.25
Y = randn(100,1);        % expected mean 0 
[~,pvalue_from_test,~,stats] = ttest(X,Y)

% set-up a bootstrap under the null, i.e. no difference
Xb        = X-mean(X); % mean is 0
Yb        = Y-mean(Y); % mean is 0
resamples = randi(100,100,10000); % make 10000 resamples with replacement 
[~,pnull,~,statsb] = ttest(Xb(resamples),Yb(resamples)); % compute 10000 ttests

% the probability distribution of t values under the null for df = 99 is
figure('Name','t distribution');
set(gcf,'Color','w','InvertHardCopy','off', 'units','normalized','outerposition',[0 0 1 1])
subplot(1,2,1); histogram(statsb.tstat,'Normalization','pdf'); grid on; box on;
hold on; plot([-3.5:0.5:3.5],tpdf([-3.5:0.5:3.5],99),'LineWidth',2) % add theoretical pdf
title('empirical and theoretical probability density funtion (tpdf)');  xlabel('t values'); ylabel('frequency');

% a p-value is the probability of observing t or bigger given the cumulative
% probability function of t values under the null, i.e. sort t-values and
% count how many are 'above' observed t
sorted_values = sort(statsb.tstat);
subplot(1,2,2); plot(sorted_values,'LineWidth',2); grid on; box on;
[~,position]=min(abs(sorted_values - stats.tstat)); % the closest empirical null to observed
hold on; plot(position+1,stats.tstat,'o','MarkerSize',8,'MarkerFaceColor','r')
l=xline(position,'-r','Count up to here','LineWidth',2); l.LabelHorizontalAlignment ='left';
title('empirical cumulative densitity function (tcdf)');  xlabel('observations'); 
ylabel('t values'); axis([-1 10010 -3.5 3.5])
for x=1:20:position-10
    plot([x x],[-3.5 sorted_values(x)-0.05],'-c')
end

pvalue_from_boot = sum(sorted_values>stats.tstat)/10000;
pvalue_from_boot = 2*min([1-pvalue_from_boot,pvalue_from_boot]);

% note that if one knows or expect the observed t value to be bigger than
% or smaller than, this is a one sided t-test and thus the p-value from the
% boostrap is sum(sorted_values>stats.tstat)/10000 or sum(sorted_values<stats.tstat)/10000
% since we did not specify, it is a two sided t-test, that is testing
% simultaneously if bigger or smaller, hence the multiplication by 2

fprintf('theoretical p-value %g, empirical p-value %g\n',pvalue_from_test,pvalue_from_boot)

%% Misconceptions

% The p-value is not an indication of the strength or magnitude of an effect, 
% because while p-values are randomly distributed when there is no effect,
% their distribution depends of both the population effect size and the 
% number of participants, making impossible to infer strength of effect from them.
figure('Name','p-values distribution');
set(gcf,'Color','w','InvertHardCopy','off', 'units','normalized','outerposition',[0 0 1 1])
subplot(1,3,1); histogram(pnull,'Normalization','pdf'); grid on; box on;
l=yline(0.05,'-r','threshold','LineWidth',2);
title('p-values distribution under H0',sprintf('%g%% under threshold',mean(pnull<.05)))

% effect of effect size and participants
effect_index = 1;
for effect = 0.1:0.2:1 % expected effect 0.1, 0.3, 0.5, 0.7, 0.9
    n_index = 1;
    for N=10:50:1000 % at each turn, increase by 20 participants
        for MC = 1:100 % do it 100 times and take the average to avoid weird variations
            X = randn(N,1) + effect;
            Y = randn(N,1);
            [~,p(effect_index,n_index,MC)]  = ttest(X(1:N),Y(1:N));
            pooled_variance    = sqrt(((N-1)*var(X(1:N))+(N-1)*var(Y(1:N)))/(length(1:N)*2-2));
            ef(MC) = (mean(X(1:N))-mean(Y(1:N)))/pooled_variance; % Cohens'd formula
        end
        pvalues(effect_index,n_index) = mean(squeeze(p(effect_index,n_index,:)));
        effect_size(effect_index,n_index) = mean(ef);
        n_index = n_index+1;
    end
    effect_index = effect_index+1;
end

subplot(1,3,2); 
histogram(p(:),'Normalization','pdf'); 
grid on; box on;
l=yline(0.05,'-r','threshold','LineWidth',2);
title('p-values distribution under H1')

subplot(1,3,3); hold on; N=10:50:1000; 
for effect = 1:size(pvalues,1)
    plot(N,pvalues(effect,:),'LineWidth',2);
end
grid on; box on; title('p-vales per sample size','for different effect sizes');
legend({'0.1','0.3','0.5','0.7','.09'})

% The p-value is not the probability of the null hypothesis p(H0), of being true,
% ->confusion between the probability of an observation given the null p(Obs≥t|H0) 
% and the probability of the null given an observation p(H0|Obs≥t) that is then taken
% as an indication for p(H0) 

MC   = 10000;
rate = 10/100;

for m=1:MC
    if m < MC*rate  % p(H0|data) is 10%
        X = randn(100,1) ; 
        Y = randn(100,1);       
    else
        X = randn(100,1) + 0.25; % expected mean 0.25
        Y = randn(100,1);        % expected mean 0
    end
    [~,pvalue(MC)] = ttest(X,Y);
end

figure('Name','p values are not P(H0|data)');
set(gcf,'Color','w','InvertHardCopy','off', 'units','normalized','outerposition',[0 0 1 1])
histogram(pvalue,'Normalization','pdf'); grid on; box on; 
title('p-values with 10% H0 true',sprintf('p-value not rejecting H0 %g%%',mean(pvalue>0.05)*100))

