using Microsoft.SCOPE.Types;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using ScopeRuntime;

using Newtonsoft.Json;

using StringNormalization;



public class PatternProcessor : Processor // This is the processor only mine n.+be+adj. pattern
{
	private bool English(string word)
	{
		foreach (char ch in word)
		{
			if (ch < 'a' || ch > 'z')
			{
				return false;
			}
		}
		return true;
	}
	public override Schema Produces(string[] requestedColumns, string[] args, Schema input)
	{
		Schema output = new Schema();
		output.Add(new ColumnInfo("Adjective", ColumnDataType.String));
		output.Add(new ColumnInfo("Noun", ColumnDataType.String));
		output.Add(new ColumnInfo("Count", ColumnDataType.Integer));
		return output;
	}
	public override IEnumerable<Row> Process(RowSet input, Row outputRow, string[] args)
	{
		Regex rg = new Regex("is|are|am|be|was|were");
		foreach (Row row in input.Rows)
		{
			string sentence = row["Sentence"].String;
			int[] tkss = JsonConvert.DeserializeObject<int[]>(row["TokenStarts"].String);
			int[] tkes = JsonConvert.DeserializeObject<int[]>(row["TokenEnds"].String);
			string[] poses = JsonConvert.DeserializeObject<string[]>(row["POSTags"].String);
			for (int i = 1; i < tkss.Length - 1; i++)
			{
				string prev_word = sentence.Substring(tkss[i - 1], tkes[i - 1] - tkss[i - 1]).ToLower();
				string mid_word = sentence.Substring(tkss[i], tkes[i] - tkss[i]).ToLower();
				string succ_word = sentence.Substring(tkss[i + 1], tkes[i + 1] - tkss[i + 1]).ToLower();
				prev_word = StringNormalization.StringNormalization.MediateNormalization(prev_word);
				mid_word = StringNormalization.StringNormalization.MediateNormalization(mid_word);
				succ_word = StringNormalization.StringNormalization.MediateNormalization(succ_word);
				if (String.IsNullOrEmpty(prev_word) || String.IsNullOrEmpty(succ_word) || String.IsNullOrEmpty(mid_word))
				{
					continue;
				}
				if (poses[i - 1].StartsWith("NN") && poses[i + 1].StartsWith("JJ") && poses[i].StartsWith("VB"))
				{
					var m = rg.Match(mid_word);
					if (m.Success)
					{
						if (!English(succ_word) || !English(prev_word))
						{
							continue;
						}
						outputRow["Adjective"].Set(succ_word);
						outputRow["Noun"].Set(prev_word);
						outputRow["Count"].Set(1);				
						yield return outputRow;
					}
				}
			}
		}
	}
}

public class DebugPatternProcessor : Processor 
{
	private bool English(string word)
	{
		foreach (char ch in word)
		{
			if (ch < 'a' || ch > 'z')
			{
				return false;
			}
		}
		return true;
	}
	public override Schema Produces(string[] requestedColumns, string[] args, Schema input)
	{
		Schema output = new Schema();
		output.Add(new ColumnInfo("Adjective", ColumnDataType.String));
		output.Add(new ColumnInfo("Noun", ColumnDataType.String));
		output.Add(new ColumnInfo("Count", ColumnDataType.Integer));
		return output;
	}
	public override IEnumerable<Row> Process(RowSet input, Row outputRow, string[] args)
	{
		Regex rg = new Regex("is|are|am|be|was|were");
		foreach (Row row in input.Rows)
		{
			string sentence = row["Sentence"].String;
			int[] tkss = JsonConvert.DeserializeObject<int[]>(row["TokenStarts"].String);
			int[] tkes = JsonConvert.DeserializeObject<int[]>(row["TokenEnds"].String);
			string[] poses = JsonConvert.DeserializeObject<string[]>(row["POSTags"].String);
			for (int i = 1; i < tkss.Length - 1; i++)
			{
				string prev_word = sentence.Substring(tkss[i - 1], tkes[i - 1] - tkss[i - 1]).ToLower();
				string mid_word = sentence.Substring(tkss[i], tkes[i] - tkss[i]).ToLower();
				string succ_word = sentence.Substring(tkss[i + 1], tkes[i + 1] - tkss[i + 1]).ToLower();
				prev_word = StringNormalization.StringNormalization.MediateNormalization(prev_word);
				mid_word = StringNormalization.StringNormalization.MediateNormalization(mid_word);
				succ_word = StringNormalization.StringNormalization.MediateNormalization(succ_word);
				if (String.IsNullOrEmpty(prev_word) || String.IsNullOrEmpty(succ_word) || String.IsNullOrEmpty(mid_word))
				{
					continue;
				}
				if (poses[i - 1].StartsWith("NN") && poses[i + 1].StartsWith("JJ") && poses[i].StartsWith("VB"))
				{
					var m = rg.Match(mid_word);
					if (m.Success)
					{
						if (!English(succ_word) || !English(prev_word))
						{
							continue;
						}
						outputRow["Adjective"].Set(succ_word);
						outputRow["Noun"].Set(prev_word);
						outputRow["Count"].Set(1); 
						yield return outputRow;
					}
				}
			}
		}
	}
}