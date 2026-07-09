# Cost Note for Learning Deployments

## Important Disclaimer

This is a learning and demonstration project. The cost information provided is for reference only. Always verify current pricing and limits with official Microsoft documentation.

## Cost Considerations

- **Azure Free Tier:** Provides 1 million free requests and 400,000 GB-seconds of compute per month for Azure Functions.
- **Trial Subscription:** Offers $200 credit for 30 days.
- **Storage:** Azure Blob Storage includes free tier limits; small submissions in a learning context will typically remain within free limits.

## Responsible Usage for Zero Cost

Responsible free-tier usage may keep total cost at zero for small demo deployments:
- Test submissions only (< 1000 requests/month)
- Small JSON payloads (< 1 KB each)
- Single blob container
- No additional monitoring or redundancy

## Steps to Minimize Cost

1. **Set an Azure Budget Alert:**
   ```bash
   az billing budget create \
	 --name learning-budget \
	 --amount 10 \
	 --category cost
   ```

2. **Use Consumption Plan:** Already configured. You pay only for executions.

3. **Delete Resources After Demo:**
   ```bash
   az group delete --name rg-student-submissions --yes
   ```

4. **Monitor Usage:** Check Azure Portal Cost Management regularly.

## What May Incur Charges

- **Exceeding free tier limits:** > 1 million requests/month for Functions
- **Storage overage:** > 5 GB blob storage
- **Outbound data transfer:** Egress to internet
- **Application Insights:** If logging is enabled beyond free tier
- **Premium plan upgrade:** Only if you change the plan

## Licensing and Power Automate

- Power Automate HTTP connector access may depend on your tenant license and plan.
- Power Apps and Dataverse licensing are separate.
- Consult your organization's Microsoft 365 licensing agreement.

## Always Verify

- Check [Azure pricing page](https://azure.microsoft.com/en-us/pricing/details/functions/) for latest rates
- Check [Azure free tier](https://azure.microsoft.com/en-us/free/) for current limits
- Use [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) to estimate costs
- Set budget alerts in Azure Portal
- Review monthly invoice in Microsoft Cost Management

## Next Steps After Demo

After completing this learning project:

1. Review total costs in Azure Cost Analysis
2. If no longer needed, delete the resource group
3. SaveScreenshots / artifacts to portfolio evidence
4. Consider future enhancements with managed identity, alerting, or CI/CD
